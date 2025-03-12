import discord
from discord import app_commands
from discord.ext import commands

class pingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @bot.tree.command(name="ping", description="latency check")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def ping(interaction: discord.Interaction):
            await interaction.response.send_message(f"<a:loading:1347935730441130074> latency: {round(bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(pingCog(bot))
