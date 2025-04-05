import discord
from discord import app_commands
from discord.ext import commands
import logic.rndm as rndm

class ballCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="8ball", description="ask the 8ball a question")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        question="question u want to ask",
        private="make the response visible only to you"
    )
    @app_commands.choices(private=[
        app_commands.Choice(name="yes", value="true"),
        app_commands.Choice(name="no", value="false")
    ])
    async def ball(self, interaction: discord.Interaction, question: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")
        result = rndm.ball_responses(question)
        await interaction.followup.send(result)

async def setup(bot):
    await bot.add_cog(ballCog(bot))