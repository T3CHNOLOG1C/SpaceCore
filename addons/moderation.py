from discord import Member
from discord.errors import Forbidden
from discord.ext import commands

from addons.utils.logger import Logger

class Moderation:
    """
    Moderation commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.modlog = Logger(__name__, bot.modlogs_channel)

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: Member, *, reason: str=None):
        """Kick a member. (Staff Only)"""
        if member == ctx.message.author:
            await ctx.send("You cannot kick yourself")
            self.modlog.info(f"{ctx.message.author.name} tried kicking themselfs")
            return

        elif member == ctx.me:
            await ctx.send("Unable to kick myself")
            self.modlog.info(f"{ctx.message.author.name} tried kicking {member.name} (Bot)")
            return

        elif self.bot.owner_role in member.roles:
            await ctx.send("Unable to kick Owner")
            self.modlog.info(f"{ctx.message.author.name} tried kicking {member.name} (Missing Permissions)")
            return

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to kick Admin")
            self.modlog.info(f"{ctx.message.author.name} tried kicking {member.name} (Missing Permissions)")
            return

        msg = f"You have been kicked from {ctx.guild.name}"
        if reason:
            msg += f" for the following reason:\n{reason}"

        try:
            await member.send(msg)
        except Forbidden:
            if not member.bot:
                await ctx.send("User had DMs disabled")

        try:
            await member.kick()
        except Forbidden:
            await ctx.send("Unable to kick Member")
            return

        await ctx.send(f"{member.name} has been kicked")
        self.modlog.info(f"{ctx.message.author.name} kicked {member.name}")

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: Member, *, reason: str=None):
        """Ban a member. (Staff Only)"""
        if member == ctx.message.author:
            await ctx.send("You cannot ban yourself")
            self.modlog.info(f"{ctx.message.author.name} tried kicking themselfs")
            return

        elif member == ctx.me:
            await ctx.send("Unable to ban myself")
            self.modlog.info(f"{ctx.message.author.name} tried kicking {member.name} (Bot)")
            return

        elif self.bot.owner_role in member.roles:
            await ctx.send("Unable to ban Owner")
            self.modlog.info(f"{ctx.message.author.name} tried banning {member.name} (Missing Permissions)")
            return

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to ban Admin")
            self.modlog.info(f"{ctx.message.author.name} tried banning {member.name} (Missing Permissions)")
            return

        msg = f"You have been banned from {ctx.guild.name}"
        if reason:
            msg += f" for the following reason:\n{reason}"

        try:
            await member.send(msg)
        except Forbidden:
            if not member.bot:
                await ctx.send("User had DMs disabled")

        try:
            await member.ban(delete_message_days=0)
        except Forbidden:
            await ctx.send("Unable to ban Member")
            return

        await ctx.send(f"{member.name} has been banned")
        self.modlog.info(f"{ctx.message.author.name} banned {member.name}")


def setup(bot):
    bot.add_cog(Moderation(bot))
