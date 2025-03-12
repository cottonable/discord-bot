import discord
from discord import app_commands
from discord.ext import commands
import logic.random as rndm

class coinflipCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @bot.tree.command(name="coinflip", description="heads or tails")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def coinflip(interaction: discord.Interaction):
            await interaction.response.send_message(rndm.coinflip())

async def setup(bot):
    await bot.add_cog(coinflipCog(bot))
