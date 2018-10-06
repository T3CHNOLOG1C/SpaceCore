import datetime
from discord.ext import commands


class Basecmds:
    """
    Base commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))

    @commands.command(hidden=True)
    async def unload(self, ctx, addon: str):
        """Unloads an addon."""
        usr = ctx.message.author
        if self.bot.admin_role in usr.roles or self.bot.owner_role in usr.roles:
            try:
                addon = "addons." + addon
                self.bot.unload_extension(addon)
                await ctx.send('✅ Addon unloaded.')
            except Exception as e:
                await ctx.send('💢 Error trying to unload the addon:\n```\n{}: {}\n```'.format(type(e).__name__, e))

    @commands.command(name='reload', aliases=['load'], hidden=True)
    async def reload(self, ctx, addon: str):
        """(Re)loads an addon."""
        usr = ctx.message.author
        if self.bot.admin_role in usr.roles or self.bot.owner_role in usr.roles:
            try:
                addon = "addons." + addon
                self.bot.unload_extension(addon)
                self.bot.load_extension(addon)
                await ctx.send('✅ Addon reloaded.')
            except Exception as e:
                await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Pong!"""
        mtime = ctx.message.created_at
        currtime = datetime.datetime.now()
        latency = currtime - mtime
        ptime = str(latency.microseconds / 1000.0)
        return await ctx.send(":ping_pong:! Pong! Response time: {} ms".format(ptime))


def setup(bot):
    bot.add_cog(Basecmds(bot))
