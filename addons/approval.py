from discord import Member, errors
from botconfig import approvalSystemEnabled
from discord.errors import Forbidden
from discord.ext import commands

from addons.utils.logger import Logger


class Approval(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.modlog = Logger(__name__, bot.modlogs_channel)

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def approve(self, ctx, member: Member):
        """Approve members"""

        if self.bot.approved_role in member.roles:
            await ctx.send("Member already approved")
            return

        try:
            await member.add_roles(self.bot.approved_role)
            dm_msg = "You have been approved. Welcome to {}!".format(
                ctx.guild.name)
            try:
                await member.send(dm_msg)
            except Forbidden:
                if not member.bot:
                    await ctx.send("User had DMs disabled")
            await ctx.send(":thumbsup: {} has been approved".format(member))
            self.modlog.approval(f"{ctx.message.author.name} approved {member.mention} [{member.name}]")
        except errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unapprove(self, ctx, member: Member):
        """Unapprove members"""

        if not self.bot.approved_role in member.roles:
            await ctx.send("Member not approved")
            return

        try:
            await member.remove_roles(self.bot.approved_role)
            await ctx.send(":thumbsdown: {} has been unapproved".format(member))
            self.modlog.approval(f"{ctx.message.author.name} unapproved {member.mention} [{member.name}]")
        except errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")


def setup(bot):
    if approvalSystemEnabled:
        bot.add_cog(Approval(bot))
