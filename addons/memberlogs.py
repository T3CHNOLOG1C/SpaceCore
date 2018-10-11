from discord import Embed, Colour

from botconfig import enableJoinLogs, enableLeaveLogs


class Memberlogs:
    """
    Logs member-related stuff
    """

    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        # TODO
        # compare all before and after content

        if before.nick != after.nick:
            logmsg = "✏️ Nickname change: {} ({}) --> {}\n".format(
                before.nick, after.mention, after.nick)

        elif before.name != after.name:
            logmsg = "✏️ Username change: {}#{} ({}) --> {}#{}\n".format(
                before.name, before.discriminator, after.mention, after.name, after.discriminator,)

        elif before.avatar_url != after.avatar_url:
            logmsg = "✏️ Avatar change: {} ({}) --> {}\n"

        else:
            logmsg = False  # User changed but nothing condition exists

        if logmsg:
            await self.bot.memberlogs_channel.send(logmsg)

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
