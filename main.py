#!/usr/bin/env python3.6
import os
import asyncio
import traceback
import json
import copy
from subprocess import call
from os import execv
from sys import argv

import discord
from discord.ext import commands

# Change to script's directory
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

# import config
from botconfig import (
    token, prefixes, description, helpDM, OwnerRole, AdminRole, approvalSystem, approvedRole, addons, message_logs_channel, mod_logs_channel, EnableJoinLogs, EnableLeaveLogs, member_logs_channel, ignored_chans
)

bot = commands.Bot(command_prefix=prefixes, description=description, max_messages=10000, pm_help=helpDM)

@bot.event
async def on_ready():

    for guild in bot.guilds:
        bot.guild = guild

    # Roles
    
    bot.owner_role = discord.utils.get(guild.roles, name=OwnerRole)
    bot.admin_role = discord.utils.get(guild.roles, name=AdminRole)

    if approvalSystem == True:
        bot.approved_role = discord.utils.get(guild.roles, name=approvedRole)

    bot.messagelogs_channel = discord.utils.get(guild.channels, name=message_logs_channel)
    bot.modlogs_channel = discord.utils.get(guild.channels, name=mod_logs_channel)
    bot.memberlogs_channel = discord.utils.get(guild.channels, name=member_logs_channel)


    # Notify user if an addon fails to load.
    for addon in addons:
        try:
            bot.load_extension(addon)
        except Exception as e:
            print("Failed to load {} :\n{} : {}".format(addon, type(e).__name__, e))

    bot.all_ready = True

    print("Client logged in as {}, in the following guild : {}".format(bot.user.name, guild.name))

@bot.command(hidden=True)
async def unload(ctx, addon: str):
    """Unloads an addon."""
    usr = ctx.message.author
    if bot.admin_role in usr.roles or bot.owner_role in usr.roles:
        try:
            addon = "addons." + addon
            bot.unload_extension(addon)
            await ctx.send('✅ Addon unloaded.')
        except Exception as e:
            await ctx.send('💢 Error trying to unload the addon:\n```\n{}: {}\n```'.format(type(e).__name__, e))

@bot.command(name='reload', aliases=['load'], hidden=True)
async def reload(ctx, addon : str):
    """(Re)loads an addon."""
    usr = ctx.message.author
    if bot.admin_role in usr.roles or bot.owner_role in usr.roles:
        try:
            addon = "addons." + addon
            bot.unload_extension(addon)
            bot.load_extension(addon)
            await ctx.send('✅ Addon reloaded.')
        except Exception as e:
            await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, e))

bot.run(token)