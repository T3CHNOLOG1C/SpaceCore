from discord import TextChannel, Embed, Colour
from discord.ext import commands
from botconfig import enableJoinLogs, enableLeaveLogs
from addons.utils.logger import Logger


class Memberlogs:
    """
    Logs member-related stuff
    """

    def __init__(self, bot):
        self.bot = bot
        self.memberlog = Logger(__name__, bot.memberlogs_channel)
        
    async def on_member_update(self, before, after):

        if before.nick != after.nick:
            self.memberlog.info(f"Nickname Changed: {before.nick} --> {after.nick} ({after.mention})")

        elif before.name != after.name:
            self.memberlog.info(f"Username change: {before.name}#{before.discriminator} --> {after.name}#{after.discriminator} ({after.mention})")

        ## TODO: Actually write role change logging code

        else:
            pass

    if enableJoinLogs == True:
        async def on_member_join(self, member):
            emb = Embed(title="Member Joined",
                        colour=Colour.green())
            emb.add_field(name="Member:", value=member.name, inline=True)
            emb.set_thumbnail(url=member.avatar_url)

            await self.bot.memberlogs_channel.send("", embed=emb)

    if enableLeaveLogs == True:
        async def on_member_remove(self, member):
            emb = Embed(title="Member Left",
                        colour=Colour.green())
            emb.add_field(name="Member:", value=member.name, inline=True)
            emb.set_thumbnail(url=member.avatar_url)

            await self.bot.memberlogs_channel.send("", embed=emb)


def setup(bot):
    bot.add_cog(Memberlogs(bot))
