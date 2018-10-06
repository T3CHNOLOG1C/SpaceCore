#!/usr/bin/env python3.6
import datetime
import discord
from discord.ext import commands
import botconfig

class Moderation:
    """
    Moderation commands
    """

    def __init__(self, bot):
        self.bot = bot
        print("{} addon loaded.".format(self.__class__.__name__))
    
        

def setup(bot):
    bot.add_cog(Moderation(bot))