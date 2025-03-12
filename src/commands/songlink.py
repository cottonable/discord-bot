import discord
from discord import app_commands
from discord.ext import commands
import logic.song_link as songl

class songlinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="songlink", description="display links to all platforms the song is on")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        link="insert link of the song",
        private="make the response visible only to you"
    )
    @app_commands.choices(private=[
        app_commands.Choice(name="yes", value="true"),
        app_commands.Choice(name="no", value="false")
    ])
    async def songlink(self, interaction: discord.Interaction, link: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")
        result = await songl.get_songlink_embed(link, private)
        
        if "embed" in result:
            await interaction.followup.send(
                embed=result["embed"], 
                file=result["file"], 
                view=result["view"], 
                ephemeral=result["ephemeral"]
            )
        else:
            await interaction.followup.send(
                content=result["content"], 
                ephemeral=result.get("ephemeral", False)
            )

async def setup(bot):
    await bot.add_cog(songlinkCog(bot))
