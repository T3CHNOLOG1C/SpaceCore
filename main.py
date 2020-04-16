#!/usr/bin/env python3.6
from traceback import format_exception
from os.path import dirname, realpath
from os import chdir
import discord
from discord.ext import commands

from addons.utils.logger import Logger

# Change to script's directory
path = dirname(realpath(__file__))
chdir(path)

# import config
try:
    import botconfig as botcfg
except ImportError:
        print("Bot config does is invalid or does not exist.")
        exit()

bot = commands.Bot(command_prefix=botcfg.prefixes,
                   description=botcfg.description, max_messages=10000, pm_help=botcfg.helpDM)


@bot.check_once
def blacklist(ctx):
    if ctx.message.author.id in botcfg.ignored_people:
        return False

    return True



@bot.event
async def on_ready():

    for guild in bot.guilds:
        bot.guild = guild

    # Roles

    bot.owner_role = discord.utils.get(guild.roles, name=botcfg.OwnerRole)
    bot.admin_role = discord.utils.get(guild.roles, name=botcfg.AdminRole)
    bot.mod_role = discord.utils.get(guild.roles, name=botcfg.ModRole)

    if botcfg.approvalSystemEnabled:
        bot.approved_role = discord.utils.get(guild.roles, name=botcfg.approvedRole)

    bot.messagelogs_channel = discord.utils.get(
        guild.channels, name=botcfg.messagelogs_channel)
    bot.memberlogs_channel = discord.utils.get(
        guild.channels, name=botcfg.memberlogs_channel)
    bot.modlogs_channel = discord.utils.get(
        guild.channels, name=botcfg.modlogs_channel)

    logger = Logger(__name__, bot.modlogs_channel)

    # Notify user if an addon fails to load.
    for addon in botcfg.addons:
        try:
            bot.load_extension("addons." + addon)
        except Exception as e:
            logger.warn("Failed to load {}:\n{}".format(addon, "".join(
                format_exception(type(e), e, e.__traceback__))))

    # Notify user if a spacecog fails to load.
    for addon in botcfg.cogs:
        try:
            bot.load_extension("cogs." + addon)
        except Exception as e:
            logger.warn("Failed to load {}:\n{}".format(addon, "".join(
                format_exception(type(e), e, e.__traceback__))))

    print(f"Client logged in as {bot.user.name}, in the following guild : {guild.name}")

if __name__ == "__main__":
    bot.run(botcfg.token)
