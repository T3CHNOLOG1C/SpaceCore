from discord import TextChannel
from discord.ext import commands

from addons.utils.logger import Logger


class Lockdown(commands.Cog):
    """
    Lockdown System
    """

    def __init__(self, bot):
        self.bot = bot
        self.lockmsg = ":lock: Channel locked."
        self.unlockmsg = ":unlock: Channel Unlocked"
        self.modlog = Logger(__name__, bot.modlogs_channel)

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["lock"])
    async def lockdown(self, ctx, *, reason=""):
        """
        Lock down a channel
        """
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        if reason:
            await ctx.send(self.lockmsg + f" The given reason is: {reason}")
        else:
            await ctx.send(self.lockmsg)
        self.modlog.info(f"{ctx.message.author.name} locked {ctx.message.channel.name}")

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["rlock"])
    async def remotelockdown(self, ctx, channel: TextChannel, *, reason=""):
        """
        Lock down a channel
        """
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(self.lockmsg)
        if reason:
            await channel.send(self.lockmsg + f" The given reason is: {reason}")
        else:
            await channel.send(self.lockmsg)
        self.modlog.info(f"{ctx.message.author.name} locked {ctx.message.channel.name}")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def unlock(self, ctx):
        """
        Unlock a channel
        """
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(":unlock: Channel Unlocked")
        self.modlog.info(f"{ctx.message.author.name} locked {ctx.message.channel.name}")

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=["runlock"])
    async def remoteunlock(self, ctx, channel: TextChannel):
        """
        Unlock a channel
        """
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await channel.send(self.unlockmsg)
        await ctx.send(self.unlockmsg)
        self.modlog.info(f"{ctx.message.author.name} locked {ctx.message.channel.name}")


def setup(bot):
    bot.add_cog(Lockdown(bot))
