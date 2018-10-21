from discord import Member
from discord.errors import Forbidden
from discord.ext import commands


class Moderation:
    """
    Moderation commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: Member, *, reason: str=None):
        """Kick a member. (Staff Only)"""
        if member == ctx.message.author:
            await ctx.send("You cannot kick yourself")
            return

        elif member == ctx.me:
            await ctx.send("Unable to kick myself")
            return

        elif self.bot.owner_role in member.roles:
            await ctx.send("Unable to kick Owner")

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to kick Admin")

        msg = "You have been kicked from {}".format(ctx.guild.name)
        if reason:
            msg += " for the following reason:\n{}".format(reason)

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

        await ctx.send("{} has been kicked".format(member.name))

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: Member, *, reason: str=None):
        """Ban a member. (Staff Only)"""
        if member == ctx.message.author:
            await ctx.send("You cannot ban yourself")
            return

        elif member == ctx.me:
            await ctx.send("Unable to ban myself")
            return

        elif self.bot.owner_role in member.roles:
            await ctx.send("Unable to ban Owner")

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to ban Admin")

        msg = "You have been banned from {}".format(ctx.guild.name)
        if reason:
            msg += " for the following reason:\n{}".format(reason)

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

        await ctx.send("{} has been banned".format(member.name))


def setup(bot):
    bot.add_cog(Moderation(bot))
