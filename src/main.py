import discord
from discord.ext import commands
import getpass

intents = discord.Intents.default()

class prototype(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands globally.")
        except discord.HTTPException as e:
            print(f"Failed to sync commands: {e}")

bot = prototype()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with nuclear bombs :3"))
    print(f'Logged in as {bot.user}!')
    await load_cogs()
    print('All cogs loaded successfully!')
    await bot.tree.sync()

async def load_cogs():
    await bot.load_extension('commands.songlink')
    await bot.load_extension('commands.ping')
    await bot.load_extension('commands.catfact')
    await bot.load_extension('commands.coinflip')
    await bot.load_extension('commands.randomnr')
    await bot.load_extension('commands.mock')

bot_tokennnnn = getpass.getpass("paste in the bot token u goober (it wont show to prevent oopsies)")

bot.run(bot_tokennnnn)