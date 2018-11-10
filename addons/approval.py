from discord import Member, Colour, Embed, errors
from botconfig impot approvalSystemEnabled
from discord.ext import commands


class Approval:

    def __init__(self, bot):
        self.bot = bot

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
            await self.dm(member, dm_msg)
            await ctx.send(":thumbsup: {} has been approved".format(member))
            emb = Embed(title="Member Approved", colour=Colour.blue())
            emb.add_field(name="Member:", value=member, inline=True)
            emb.add_field(
                name="Mod:", value=ctx.message.author, inline=True)
            logchannel = self.bot.logs_channel
            await logchannel.send("", embed=emb)
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
            await ctx.send(":thumbsup: {} has been approved".format(member))
            emb = Embed(title="Member Unapprove", colour=Colour.blue())
            emb.add_field(name="Member:", value=member, inline=True)
            emb.add_field(
                name="Mod:", value=ctx.message.author, inline=True)
            logchannel = self.bot.logs_channel
            await logchannel.send("", embed=emb)
        except errors.Forbidden:
            await ctx.send("💢 I dont have permission to do this.")


def setup(bot):
    if approvalSystemEnabled:
        bot.add_cog(Approval(bot))
