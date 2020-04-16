from discord import Embed, Colour
from discord.ext import commands
from botconfig import enableJoinLogs, enableLeaveLogs
from addons.utils.logger import Logger


class Memberlogs(commands.Cog):
    """
    Logs member-related stuff
    """

    def __init__(self, bot):
        self.bot = bot
        self.memberlog = Logger(__name__, bot.memberlogs_channel)


    @commands.Cog.listener()    
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            self.memberlog.info(f"Nickname Changed: {before.nick} --> {after.nick} ({after.mention})")

        if before.name != after.name:
            self.memberlog.info(f"Username change: {before.name}#{before.discriminator} --> {after.name}#{after.discriminator} ({after.mention})")

        if before.roles != after.roles:
            before_roles = []
            after_roles = []

            for role in before.roles:
                before_roles.append(role.name)

            for role in after.roles:
                after_roles.append(role.name)
            
            if before.roles>after.roles:
                set_difference = set(after_roles) - set(before_roles)
                x = set_difference.pop()
                role_string = "+ " + x
                self.memberlog.info(f"Change in roles for {after.name}:\n {role_string}")
            else:
                set_difference = set(before_roles) - set(after_roles)
                x = set_difference.pop()
                role_string = "- " + x
                self.memberlog.info(f"Change in roles for {after.name}:\n {role_string}")
                

        else:
            pass

    if enableJoinLogs == True:
        @commands.Cog.listener()
        async def on_member_join(self, member):
            emb = Embed(title="Member Joined",
                        colour=Colour.green())
            emb.add_field(name="Member:", value=member.name, inline=True)
            emb.set_thumbnail(url=member.avatar_url)

            await self.bot.memberlogs_channel.send("", embed=emb)

    if enableLeaveLogs == True:
        @commands.Cog.listener()
        async def on_member_remove(self, member):
            emb = Embed(title="Member Left",
                        colour=Colour.green())
            emb.add_field(name="Member:", value=member.name, inline=True)
            emb.set_thumbnail(url=member.avatar_url)

            await self.bot.memberlogs_channel.send("", embed=emb)


def setup(bot):
    bot.add_cog(Memberlogs(bot))
