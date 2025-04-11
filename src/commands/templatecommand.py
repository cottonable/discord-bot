import discord
from discord import app_commands
from discord.ext import commands

class commandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="command", description="description")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        message="1",
        private="2"
    )
    @app_commands.choices(private=[
        app_commands.Choice(name="yes", value="true"),
        app_commands.Choice(name="no", value="false")
    ])
    async def randomnr(self, interaction: discord.Interaction, message: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")
        await interaction.followup.send(message)

async def setup(bot):
    await bot.add_cog(commandCog(bot))
