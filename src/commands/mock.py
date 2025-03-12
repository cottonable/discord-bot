import discord
from discord import app_commands
from discord.ext import commands

class mockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="mock", description="generate a mock string")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        string="string u want to mock",
        private="make the response visible only to you"
    )
    @app_commands.choices(private=[
        app_commands.Choice(name="yes", value="true"),
        app_commands.Choice(name="no", value="false")
    ])
    async def mock(self, interaction: discord.Interaction, string: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")
        result = mock_logic(string)
        await interaction.followup.send(result)

async def setup(bot):
    await bot.add_cog(mockCog(bot))

# LOGIC
def mock_logic(string):
    return ''.join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(string))