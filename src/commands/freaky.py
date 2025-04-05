import discord
from discord import app_commands
from discord.ext import commands

class freakyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="freaky", description="freakify your text")
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(
        tofreakify="text to freakify",
        private="make the response visible only to you"
    )
    @app_commands.choices(private=[
        app_commands.Choice(name="yes", value="true"),
        app_commands.Choice(name="no", value="false")
    ])
    async def ball(self, interaction: discord.Interaction, tofreakify: str, private: str = "false"):
        await interaction.response.defer(ephemeral=private.lower() == "true")
        result = freakinator5000(tofreakify)
        await interaction.followup.send(result)

async def setup(bot):
    await bot.add_cog(freakyCog(bot))
    
def freakinator5000(tofreakify):
    normal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    fancy = '𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩'
    return ''.join([fancy[normal.index(c)] if c in normal else c for c in tofreakify])