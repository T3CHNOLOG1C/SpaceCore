from discord.ext import commands
from discord import Member, Embed
from time import time

from addons.utils.logger import Logger
from addons.utils.config import Config


class Warn:
    """
    Warning System
    """

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger(__name__, bot.memberlogs_channel)
        self.config = Config("warn", {'users': {}})

    @commands.command()
    async def warn(self, ctx, member: Member, *, reason: str=""):
        if member == ctx.message.author:
            await ctx.send("You cannot warn yourself")
            return

        elif member == ctx.me:
            await ctx.send("Unable to warn myself")
            return

        elif self.bot.owner_role in member.roles:
            await ctx.send("Unable to warn Owner")
            return

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to warn Admin")
            return

        currentTime = time()

        if not member.id in self.config.users:
            self.config.users[member.id] = []

        self.config.users[member.id].append(
            (reason, ctx.message.author.id, currentTime))

        await ctx.send("User warned")

        self.config.save()
        self.logger.info(f"{ctx.message.author.name} warned {member.name}")

    @commands.command(aliases=["unwarn"])
    async def delwarn(self, ctx, member: Member, number: int):
        if member == ctx.message.author:
            await ctx.send("You cannot unwarn yourself")
            return

        elif self.bot.owner_role in member.roles:
            await ctx.send("Unable to unwarn Owner")
            return

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to unwarn Admin")
            return

        if not member.id in self.config.users:
            await ctx.send("User has no warns")
            return

        if not len(self.config.users[member.id]) >= number:
            await ctx.send("No such warn")
            return

        self.config.users[member.id].pop(number)

        await ctx.send("User unwarned")

        self.config.save()
        self.logger.info(f"{ctx.message.author.name} unwarned {member.name}")

    @commands.command()
    async def listwarns(self, ctx, member: Member):
        if not member.id in self.config.users:
            await ctx.send("User has no warns")
            return

        embed = Embed(color=member.colour)

        for nr, warn in enumerate(self.config.users[member.id]):
            content = (f"Reason:   {warn[0]}\n"
                       f"Moderator:{warn[1]}\n"
                       f"Time: {warn[2]}")  # TODO convert Unix time to local time
            embed.addfield(name=nr, value=content)

        await ctx.send("", embed=embed)


def setup(bot):
    bot.add_cog(Warn(bot))
