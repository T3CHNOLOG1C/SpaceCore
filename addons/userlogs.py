import discord
from botconfig import enableJoinLogs, enableLeaveLogs


class Userlogs:
    """
    bot events
    """

    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        # Log nickname changes to the dedicated channel.
        logchannel = self.bot.memberlogs_channel
        if before.nick != after.nick:
            logmsg = "✏️ Nickname change: {} ({}) --> {}".format(
                before.nick, after.mention, after.nick)
            await logchannel.send(logmsg)
        # If the member's nickname didn't change, check if their username
        # changed.
        elif before.name != after.name:
            logmsg = "✏️ Username change: {}#{} ({}) --> {}#{}".format(
                before.name, before.discriminator, after.mention, after.name, after.discriminator,)
            await logchannel.send(logmsg)

    if enableJoinLogs == True:
        async def on_member_join(self, member):
            user = member
            emb = discord.Embed(title="Member Joined",
                                colour=discord.Colour.green())
            emb.add_field(name="Member:", value=member.name, inline=True)
            emb.set_thumbnail(url=user.avatar_url)
            logchannel = self.bot.memberlogs_channel
            await logchannel.send("", embed=emb)

    if enableLeaveLogs == True:
        async def on_member_remove(self, member):
            user = member
            emb = discord.Embed(title="Member Left",
                                colour=discord.Colour.green())
            emb.add_field(name="Member:", value=member.name, inline=True)
            emb.set_thumbnail(url=user.avatar_url)
            logchannel = self.bot.memberlogs_channel
            await logchannel.send("", embed=emb)


def setup(bot):
    bot.add_cog(Userlogs(bot))
