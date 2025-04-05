import discord
from discord import app_commands
from discord.ext import commands
import logic.song_link as songl
import logic.album_link as albuml

class odesliCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="odesli", description="display links to all platforms the song/album is on")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        type="type of the link",
        link="insert link of the song/album",
        private="make the response visible only to you"
    )
    @app_commands.choices(type=[
        app_commands.Choice(name="song", value="song"),
        app_commands.Choice(name="album", value="album")
    ])
    @app_commands.choices(private=[
    app_commands.Choice(name="yes", value="true"),
    app_commands.Choice(name="no", value="false")
    ])
    async def odesli(self, interaction: discord.Interaction, type: str, link: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")
        
        if type == "album":
            result = await albuml.get_albumlink_embed(link, private)
        else:
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
    await bot.add_cog(odesliCog(bot))
