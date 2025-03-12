import discord
from discord import app_commands
from discord.ext import commands
import logic.random as rndm

class randomnrCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="randomnr", description="generate a random number between two numbers")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        fromnr="from what number",
        tonr="to what number",
        private="make the response visible only to you"
    )
    @app_commands.choices(private=[
        app_commands.Choice(name="yes", value="true"),
        app_commands.Choice(name="no", value="false")
    ])
    async def randomnr(self, interaction: discord.Interaction, fromnr: str, tonr: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")
        result = rndm.random_number(fromnr, tonr)
        await interaction.followup.send(result)

async def setup(bot):
    await bot.add_cog(randomnrCog(bot))
