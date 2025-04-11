import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import re
import datetime
import json
import os
from typing import Dict, List, Tuple

class RemindLogic:
    def __init__(self, bot):
        self.bot = bot
        self.active_reminders = {}  # user_id -> [(time, message), ...]
        self.save_file = "data/reminders.json"
        self._ensure_data_directory()

        # schedule loading reminders when bot is ready
        bot.loop.create_task(self._delayed_load_reminders())

    def _ensure_data_directory(self):
        # create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)

    async def _delayed_load_reminders(self):
        # wait for bot to be fully ready before loading reminders
        await self.bot.wait_until_ready()
        await self._load_reminders()

    async def _load_reminders(self):
        # load reminders from file on startup
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)

                # convert string keys to integers
                for user_id_str, reminders in data.items():
                    user_id = int(user_id_str)
                    self.active_reminders[user_id] = []

                    for reminder in reminders:
                        # parse saved data
                        time_str = reminder[0]
                        message = reminder[1]
                        reminder_time = datetime.datetime.fromisoformat(time_str)

                        # only load reminders that haven't happened yet
                        now = datetime.datetime.now()
                        if reminder_time > now:
                            self.active_reminders[user_id].append((reminder_time, message))

                            # schedule the reminder
                            seconds = max(0, (reminder_time - now).total_seconds())
                            asyncio.create_task(self._handle_reminder(
                                user_id, reminder_time, message, seconds))

                print(f"loaded {sum(len(r) for r in self.active_reminders.values())} active reminders")
        except Exception as e:
            print(f"failed to load reminders: {e}")
            self.active_reminders = {}  # start with empty reminders

    def _save_reminders(self):
        # save reminders to persistent storage
        try:
            data = {}
            for user_id, reminders in self.active_reminders.items():
                # sort reminders by time before saving
                sorted_reminders = sorted(reminders, key=lambda x: x[0])
                data[str(user_id)] = [(time.isoformat(), message) for time, message in sorted_reminders]

            with open(self.save_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"error saving reminders: {e}")

    async def parse_time(self, time_str: str) -> int:
        # parse time string into seconds
        time_pattern = re.compile(r"^(\d+)([smhd])$")
        match = time_pattern.match(time_str.lower())

        if not match:
            raise ValueError("Invalid time format. Use format like 5m, 2h, 1d")

        amount, unit = match.groups()
        amount = int(amount)

        # convert to seconds
        if unit == 's':
            return amount
        elif unit == 'm':
            return amount * 60
        elif unit == 'h':
            return amount * 3600
        elif unit == 'd':
            return amount * 86400

    async def set_reminder(self, user_id: int, message: str, seconds: int) -> datetime.datetime:
        # create a new reminder
        reminder_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

        if user_id not in self.active_reminders:
            self.active_reminders[user_id] = []

        self.active_reminders[user_id].append((reminder_time, message))

        # save to file
        self._save_reminders()

        # schedule the reminder task
        asyncio.create_task(self._handle_reminder(user_id, reminder_time, message, seconds))

        return reminder_time

    async def _handle_reminder(self, user_id: int, reminder_time: datetime.datetime, message: str, seconds: int):
        # wait for the reminder time and then notify the user
        await asyncio.sleep(seconds)

        # send the reminder dm
        try:
            # try cache first
            user = self.bot.get_user(user_id)

            # if not in cache, fetch from api
            if user is None:
                user = await self.bot.fetch_user(user_id)

            if user:
                embed = discord.Embed(
                    title="Reminder",
                    description=message,
                    color=discord.Color.blue()
                )
                embed.timestamp = discord.utils.utcnow()

                await user.send(embed=embed)
            else:
                print(f"could not find user {user_id} for reminder")

        except discord.errors.Forbidden:
            # can't dm user
            print(f"user {user_id} has dms disabled")
        except Exception as e:
            print(f"error sending reminder to {user_id}: {e}")

        # remove the completed reminder
        if user_id in self.active_reminders:
            try:
                self.active_reminders[user_id].remove((reminder_time, message))
                if not self.active_reminders[user_id]:
                    del self.active_reminders[user_id]
                # update stored data
                self._save_reminders()
            except ValueError:
                # reminder might have been removed already
                pass

    async def get_active_reminders(self, user_id: int) -> List[Tuple[datetime.datetime, str]]:
        # get all active reminders for a user
        if user_id in self.active_reminders:
            # return sorted by time
            return sorted(self.active_reminders[user_id], key=lambda x: x[0])
        return []

    async def cancel_reminder(self, user_id: int, index: int) -> bool:
        # cancel a specific reminder by index
        reminders = await self.get_active_reminders(user_id)

        if 0 <= index < len(reminders):
            reminder_to_remove = reminders[index]
            self.active_reminders[user_id].remove(reminder_to_remove)

            if not self.active_reminders[user_id]:
                del self.active_reminders[user_id]

            # update saved data
            self._save_reminders()
            return True
        return False
