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
from botconfig import (token, prefixes, description, helpDM, OwnerRole, AdminRole, approvalSystemEnabled,
                       approvedRole, addons, messagelogs_channel, memberlogs_channel, modlogs_channel)

bot = commands.Bot(command_prefix=prefixes,
                   description=description, max_messages=10000, pm_help=helpDM)


@bot.event
async def on_ready():

    for guild in bot.guilds:
        bot.guild = guild

    # Roles

    bot.owner_role = discord.utils.get(guild.roles, name=OwnerRole)
    bot.admin_role = discord.utils.get(guild.roles, name=AdminRole)

    if approvalSystemEnabled == True:
        bot.approved_role = discord.utils.get(guild.roles, name=approvedRole)

    bot.messagelogs_channel = discord.utils.get(
        guild.channels, name=messagelogs_channel)
    bot.memberlogs_channel = discord.utils.get(
        guild.channels, name=memberlogs_channel)
    bot.modlogs_channel = discord.utils.get(
        guild.channels, name=modlogs_channel)

    # Setup Logger

    logger = Logger(__name__, bot.modlogs_channel)

    # Notify user if an addon fails to load.
    for addon in addons:
        try:
            bot.load_extension(addon)
        except Exception as e:
            logger.warn("Failed to load {}:\n{}".format(addon, "".join(
                format_exception(type(e), e, e.__traceback__))))

    print("Client logged in as {}, in the following guild : {}".format(
        bot.user.name, guild.name))

if __name__ == "__main__":
    bot.run(token)
