from pylast import LastFMNetwork, LibreFMNetwork, WSError
from addons.utils.logger import Logger
from addons.utils.config import Config

from discord import Member
from discord.ext import commands


class LastFM:
    """
    Show others what you are listening to
    """

    def __init__(self, bot):
        self.bot = bot

        self.logger = Logger(__name__, bot.modlogs_channel)
        self.config = Config("lastfm", {"users": {}, 'api': {
                             'lastfm': ['', ''], 'librefm': ['', '']}})

        self.network = {}
        self.network['lastfm'] = LastFMNetwork(
            self.config.api['lastfm'][0], self.config.api['lastfm'][1])
        self.network['librefm'] = LibreFMNetwork(self.config.api['lastfm'][0], self.config.api[
                                                 'lastfm'][1])  # LibreFM requires no API keys, keeping this incase that ever changes

    def isnetwork(self, value):
        cond1 = any(self.network[value].api_key)
        cond2 = any(self.network[value].api_secret)

        return cond1 and cond2

    @commands.group(name="set")
    async def setservice(self, ctx):
        if ctx.invoked_subcommand is None:
            pages = await self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await ctx.send(page)

    @setservice.command()
    async def lastfm(self, ctx, username):
        """Link your LastFM account to your Discord account"""
        try:
            self.network['lastfm'].get_user(username).get_now_playing()
            self.config.users[str(ctx.message.author.id)] = [
                username, "lastfm"]
            self.config.save()
            await ctx.send(f"Set your LastFM account to {username}")
        except WSError:
            if self.isnetwork('lastfm'):
                await ctx.send("User does not exist")
            else:
                await ctx.send("Addon has not been properly setup.")
                self.logger.warn("Key or Secret not setup")

    @setservice.command()
    async def librefm(self, ctx, username):
        """Link your LibreFM account to your Discord account"""
        try:
            self.network['librefm'].get_user(username).get_now_playing()
            self.config.users[str(ctx.message.author.id)] = [
                username, "librefm"]
            self.config.save()
            await ctx.send(f"Set your LibreFM account to {username}")
        except WSError:
            await ctx.send("User does not exist")

    @commands.command()
    async def np(self, ctx, user: Member=None):
        if not user:
            user = ctx.message.author

        try:
            account = self.network[self.config.users[str(user.id)][1]].get_user(
                self.config.users[str(user.id)][0])
            playing = account.get_now_playing()
            if not playing:
                await ctx.send(f"{user.display_name} is playing nothing")
                return
            await ctx.send(f"{user.display_name} is playing {playing.artist.name} - {playing.title}")
        except KeyError:
            await ctx.send(f"You have no account\nPlease use `{ctx.prefix}set` to set one up")
        except WSError:
            await ctx.send(f"The account under your name is not available anymore.\nPlease use `{ctx.prefix}set` to set one up")


def setup(bot):
    bot.add_cog(LastFM(bot))
