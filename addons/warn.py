from discord.ext import commands
from discord import Member, Embed, Colour
from discord.errors import Forbidden

from json import load, dump
from time import strftime, localtime

from addons.utils.logger import Logger
from addons.utils.config import Config


class Warn:
    """
    Warning system
    """

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger(__name__, bot.memberlogs_channel)

    async def dm(self, member: Member, message: str):
        """DM the user and catch an eventual exception."""
        try:
            await member.send(message)
        except:
            pass

    @commands.has_permissions(manage_roles=True)
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

        try:
            with open("data/warns.json", "r") as config:
                js = load(config)
        except FileNotFoundError:
            with open("data/warns.json", "w") as config:
                config.write('{}')
                js = {}

        userid = str(member.id)
        if userid not in js:
            amount_of_warns = 1
            js[userid] = {"warns": []}
        else:
            amount_of_warns = len(js[userid]["warns"]) + 1

        member_name = "{}#{}".format(member.name, member.discriminator)
        timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
        author_name = "{}#{}".format(ctx.message.author.name, ctx.message.author.discriminator)

        js[userid]["amount"] = amount_of_warns
        js[userid]["warns"].append({
            "name": member_name,
            "timestamp": timestamp,
            "reason": reason,
            "author": author_name,
            "author_id": ctx.message.author.id,
        })

        try:
            await member.send(f"You have been warned in {ctx.guild.name} for the following reason: {reason}. This is warning #{amount_of_warns}.")
        except Forbidden:
            if not member.bot:
                await ctx.send("User had DMs disabled")
        await ctx.send(f"🚩 {member} has been warned. This is warning #{amount_of_warns}.")

        self.logger.info(f"{ctx.message.author.name} warned {member.name} for {reason}. (#{amount_of_warns}.")

        if amount_of_warns == 1:
            try:
                await member.send("This is your first warning.")
            except Forbidden:
                pass

        elif amount_of_warns == 2:
            try:
                await member.send("This is your second warning.\nYour next warn will result in being kicked from the server.")
            except Forbidden:
                pass
        elif amount_of_warns == 3:
            try:
                await member.send("This is your third warning, so you have been kicked. Please "
                                  "note that **the next warn will result in another kick!**")
            except Forbidden:
                pass
            await member.kick(reason="Third warn, {}".format(reason))

        elif amount_of_warns == 4:
            try:
                await member.send("You have been kicked from the server. This is your fourth and "
                                  "final warning. **__The next warning will result in an automatic"
                                      " ban.__**")
            except Forbidden:
                pass
            await member.kick(reason="Fourth warn: {}".format(reason))

        elif amount_of_warns >= 5:
            try:
                await self.dm(member, "You have reached your fifth warning. You are now "
                                      "banned from this server.")
            except Forbidden:
                pass
            await member.ban(delete_message_days=0, reason="Fifth warn: {}".format(reason))

        with open("data/warns.json", "w") as f:
            dump(js, f, sort_keys=True, indent=4, separators=(',', ': '))

    @commands.has_permissions(manage_roles=True)
    @commands.command(aliases=["unwarn", "delwarn"])
    async def deletewarn(self, ctx, member: Member, number: int):
        author = ctx.message.author
        if member == ctx.message.author:
            await ctx.send("You cannot unwarn yourself")
            return

        elif self.bot.owner_role in member.roles:
            await ctx.send("Unable to unwarn Owner")
            return

        elif self.bot.admin_role in member.roles and not self.bot.owner_role in ctx.message.author.roles:
            await ctx.send("Unable to unwarn Admin")
            return
        elif number <= 0:
            await ctx.send("Warn number has to be a positive number")
            return

        with open("data/warns.json", "r") as f:
            js = load(f)  # https://hastebin.com/ejizaxasav.scala

        userid = str(member.id)
        if userid not in js:
            js[userid] = {"warns": []}
            await ctx.send("{} doesn't have any warns.".format(member.name))
            return
        else:
            amount_of_warns = len(js[userid]["warns"]) - 1

        js[userid]["amount"] = amount_of_warns
        js[userid]["warns"].pop(number - 1)
        await ctx.send("🚩 I've deleted the {} warn of {}. The user now has {} warns."
                       "".format(number, member, amount_of_warns))
        try:
            await member.send("One of your warns in {} has been removed.".format(ctx.guild.name))
        except Forbidden:
            pass

        self.logger.info(f"{ctx.message.author.name} removed warn #{number} from {member.name}")

        with open("data/warns.json", "w") as f:
            dump(js, f, sort_keys=True, indent=4, separators=(',', ': '))


    @commands.command()
    async def listwarns(self, ctx, member: Member=None):
        """
        List your own warns or someone else's warns.
        Only the staff can view someone else's warns
        """
        if not member:
            member = ctx.message.author


        has_perms = self.bot.owner_role or self.bot.admin_role or self.bot.mod_role in ctx.message.author.roles

        if not has_perms and member != ctx.message.author:
            return await ctx.send("{} You don't have permission to list other member's warns!"
                                  "".format(ctx.message.author.mention))

        with open("data/warns.json", "r") as f:
            js = load(f)

        userid = str(member.id)
        print(userid)
        print(js)
        if userid not in js:
            return await ctx.send("No warns found!")
        embed = Embed(color=member.colour)
        embed.set_author(name="List of warns for {} :".format(
            member), icon_url=member.avatar_url)

        for nbr, warn in enumerate(js[userid]["warns"]):
            content = "{}".format(warn["reason"])
            author = await self.bot.get_user_info(warn["author_id"])
            content += "\n*Warn author : {} ({})*".format(
                warn["author"], author.mention)
            embed.add_field(name="\n\n#{}: {}".format(nbr + 1, warn["timestamp"]),
                            value=content, inline=False)

        await ctx.send("", embed=embed)

def setup(bot):
    bot.add_cog(Warn(bot))
