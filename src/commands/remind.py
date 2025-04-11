import discord
from discord import app_commands
from discord.ext import commands
import datetime
from logic.rmnd import RemindLogic

class RemindCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.remind_logic = RemindLogic(bot)

    @app_commands.command(name="remind", description="Set a reminder for yourself")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        time="When to remind you (format: 5m, 2h, 1d)",
        message="The message for your reminder",
        private="Should the response be private"
    )
    @app_commands.choices(private=[
        app_commands.Choice(name="yes", value="true"),
        app_commands.Choice(name="no", value="false")
    ])
    async def remind(self, interaction: discord.Interaction, time: str, message: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")

        try:
            seconds = await self.remind_logic.parse_time(time)

            if seconds < 5:
                await interaction.followup.send("Reminder time must be at least 5 seconds.")
                return

            reminder_time = await self.remind_logic.set_reminder(
                interaction.user.id,
                message,
                seconds
            )

            # Format the time
            time_format = reminder_time.strftime("%B %d, %Y at %I:%M %p")

            embed = discord.Embed(
                title="✅ Reminder Set",
                description=f"I'll remind you on **{time_format}**",
                color=discord.Color.green()
            )
            embed.add_field(name="Message", value=message, inline=False)

            await interaction.followup.send(embed=embed)

        except ValueError as e:
            await interaction.followup.send(f"Error: {str(e)}")

    @app_commands.command(name="reminders", description="List your active reminders")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def reminders(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        reminders = await self.remind_logic.get_active_reminders(interaction.user.id)

        if not reminders:
            await interaction.followup.send("You don't have any active reminders.")
            return

        embed = discord.Embed(
            title="Your Active Reminders",
            color=discord.Color.blue()
        )

        for i, (time, message) in enumerate(reminders):
            time_format = time.strftime("%B %d, %Y at %I:%M %p")
            embed.add_field(
                name=f"#{i+1}: {time_format}",
                value=message,
                inline=False
            )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="cancel", description="Cancel a reminder")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        index="The number of the reminder to cancel (check /reminders)"
    )
    async def cancel(self, interaction: discord.Interaction, index: int):
        await interaction.response.defer(ephemeral=True)

        # Adjust for 1-based indexing in the UI vs 0-based indexing in the code
        adjusted_index = index - 1

        success = await self.remind_logic.cancel_reminder(interaction.user.id, adjusted_index)

        if success:
            await interaction.followup.send(f"Reminder #{index} cancelled.")
        else:
            await interaction.followup.send(f"Couldn't find reminder #{index}. Use /reminders to see your active reminders.")

async def setup(bot):
    await bot.add_cog(RemindCog(bot))
