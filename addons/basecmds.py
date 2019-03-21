from datetime import datetime
from traceback import format_exception
from discord.ext import commands
from os import execl
from sys import executable, argv
from asyncio import sleep

from addons.utils.logger import Logger
from addons.utils import checks


class Basecmds:
    """
    Base commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.modlog = Logger(__name__, bot.modlogs_channel)

    @commands.command()
    @checks.is_staff()
    async def unload(self, ctx, addon: str):
        """Unloads an addon."""
        if addon == "basecmds":
            await ctx.send("Cannot unload base commands")
            return

        try:
            addon = "addons." + addon
            self.bot.unload_extension(addon)
            self.modlog.info(addon + " unloaded")
            await ctx.send('✅ Addon unloaded.')
        except Exception as e:
            self.modlog.warn("Failed to load {}: {}".format(addon, "".join(
                format_exception(type(e), e, e.__traceback__))))
            await ctx.send('💢 Error trying to unload the addon:\n```\n{}: {}\n```'.format(type(e).__name__, e))

    @commands.command(aliases=['reload'])
    @checks.is_staff()
    async def load(self, ctx, addon: str):
        """(Re)loads an addon."""
        try:
            addon = "addons." + addon
            self.bot.unload_extension(addon)
            self.bot.load_extension(addon)
            self.modlog.info(addon + " loaded")
            await ctx.send('✅ Addon reloaded.')
        except Exception as e:
            self.modlog.warn("Failed to load {}: {}".format(addon, "".join(
                format_exception(type(e), e, e.__traceback__))))
            await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        mtime = ctx.message.created_at
        currtime = datetime.now()
        latency = currtime - mtime
        ptime = str(latency.microseconds / 1000.0)
        return await ctx.send(":ping_pong:! Pong! Response time: {} ms".format(ptime))

    @commands.command(name="exit", aliases=["shutdown"])
    @checks.is_owner()
    async def _exit(self, ctx):
        """Shutdown the bot"""

        await ctx.send("Shutting down")
        self.modlog.warn(
            "Bot shutdown via command by {}".format(ctx.message.author))

        await self.bot.logout()

    @commands.command()
    @checks.is_staff()
    async def restart(self, ctx):
        """Restart the bot"""

        await ctx.send("Restarting...")
        self.modlog.info(
            "Bot restart via command by {}".format(ctx.message.author))
        await sleep(1)  # process is replaced too fast for logger

        execl(executable, 'python', "main.py", *argv[1:])


def setup(bot):
    bot.add_cog(Basecmds(bot))
