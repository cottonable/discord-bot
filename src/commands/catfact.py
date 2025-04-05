import discord
from discord import app_commands
from discord.ext import commands
import logic.rndm as rndm

class catfactCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @bot.tree.command(name="catfact", description="random cat fact")
        @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
        async def catfact(interaction: discord.Interaction):
            await interaction.response.send_message(rndm.cat_emoji() + " " + rndm.cat_fact())

async def setup(bot):
    await bot.add_cog(catfactCog(bot))
