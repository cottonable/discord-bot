import discord
from discord import app_commands
from discord.ext import commands

class sayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="say", description="make the bot say anything u want")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        message="what do u want the bot to say",
        private="make the response visible only to you"
    )
    @app_commands.choices(private=[
        app_commands.Choice(name="yes", value="true"),
        app_commands.Choice(name="no", value="false")
    ])
    async def randomnr(self, interaction: discord.Interaction, message: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")
        await interaction.followup.send(message)

async def setup(bot):
    await bot.add_cog(sayCog(bot))
