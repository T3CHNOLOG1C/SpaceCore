from discord.ext import commands
from discord.utils import get
from discord import Member
from discord.errors import Forbidden

from addons.utils.logger import Logger
from botconfig import MuteRole


class Mute:
    """
    Mute System
    """

    def __init__(self, bot):
        self.bot = bot
        self.role = get(bot.guild.roles, name=MuteRole)
        self.modlog = Logger(__name__, bot.modlogs_channel)

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, member: Member, *, reason: str=None):
        if member == ctx.message.author:
            self.modlog.info(f"{ctx.message.author.name} tried muting themselfs")
            await ctx.send("You cannot mute yourself")
            return

        elif member == ctx.me:
            await ctx.send("Unable to mute myself")
            self.modlog.info(f"{ctx.message.author.name} tried muting {member.name} (Bot)")
            return

        elif self.bot.owner_role in member.roles:
            await ctx.send("Unable to mute Owner")
            self.modlog.info(f"{ctx.message.author.name} tried muting {member.name} (Missing Permissions)")
            return

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to mute Admin")
            self.modlog.info(f"{ctx.message.author.name} tried muting {member.name} (Missing Permissions)")
            return

        elif self.role in member.roles:
            await ctx.send("User is already muted")
            self.modlog.info(f"{ctx.message.author.name} tried muting {member.name} (Already Muted)")
            return

        await member.add_roles(self.role)

        msg = f"You have been muted in {ctx.guild.name}"
        if reason:
            msg += f" for the following reason: {reason}"

        try:
            await member.send(msg)
        except Forbidden:
            if not member.bot:
                await ctx.send("User had DMs disabled")
        if reason:
            self.modlog.info(f"{ctx.message.author.name} muted {member.name} for reason: {reason}")
        else:
            self.modlog.info(f"{ctx.message.author.name} muted {member.name}")
        await ctx.send(f"{member} has been muted.")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, member: Member):
        if member == ctx.message.author:
            await ctx.send("You cannot unmute yourself")
            self.modlog.info(f"{ctx.message.author.name} tried unmuting themselfs")
            return

        elif self.bot.owner_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to unmute Owner")
            self.modlog.info(f"{ctx.message.author.name} tried unmuting {member.name} (Missing Permissions)")
            return

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to unmute Admin")
            self.modlog.info(f"{ctx.message.author.name} tried unmuting {member.name} (Missing Permissions)")
            return

        elif not self.role in member.roles:
            self.modlog.info(f"{ctx.message.author.name} tried unmuting {member.name} (Not Muted)")
            await ctx.send("User is not muted")
            return

        await member.remove_roles(self.role)
        try:
            await member.send(f"You have been unmuted in {ctx.guild.name}")
        except Forbidden:
            if not member.bot:
                await ctx.send("User had DMs disabled")
        self.modlog.info(f"{ctx.message.author.name} unmuted {member.name}")
        await ctx.send(f"{member} has been unmuted.")

def setup(bot):
    bot.add_cog(Mute(bot))
