import importlib
from datetime import datetime
from traceback import format_exception
from discord import Embed, Color
from discord.ext import commands
from os import execl
from sys import executable, argv
from asyncio import sleep

from addons.utils.logger import Logger
from addons.utils import checks
from botconfig import cogs

class Basecmds(commands.Cog):
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

    @commands.command()
    @checks.is_staff()
    async def unloadcog(self, ctx, cog: str):
        """Unloads an addon."""
        try:
            cog = "cogs." + cog
            self.bot.unload_extension(cog)
            self.modlog.info(cog + " unloaded")
            await ctx.send('✅ Cog unloaded.')
        except Exception as e:
            self.modlog.warn("Failed to load {}: {}".format(cog, "".join(
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

    @commands.command(aliases=['reloadcog'])
    @checks.is_staff()
    async def loadcog(self, ctx, cog: str):
        """(Re)loads a cog."""
        try:
            cog = "cogs." + cog
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            self.modlog.info(cog + " loaded")
            await ctx.send('✅ Cog reloaded.')
        except Exception as e:
            self.modlog.warn("Failed to load {}: {}".format(cog, "".join(
                format_exception(type(e), e, e.__traceback__))))
            await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

    @commands.command(aliases=['cogs'])
    async def listcogs(self, ctx):
        embed = Embed(color=Color.blue())
        embed.set_author(name="Loaded Cogs:")
        content = ""
        for x in cogs:
            x = "cogs." + x
            cog = importlib.import_module(x)
            name = "{} \nSource: {}\n".format(cog.cogname, cog.cogsource)
            content += "License: {}".format(cog.coglicense)
            embed.add_field(name=name, value=content)
        await ctx.send("", embed=embed)

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
