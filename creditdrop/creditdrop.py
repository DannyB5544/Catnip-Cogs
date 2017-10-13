#Import #Import Stuffios of course!
import discord
from random import randint
from discord.ext import commands
from cogs.utils.dataIO import dataIO #Maybe one day.
import asyncio
from .utils import checks
import os
from __main__ import send_cmd_help
import os
import asyncio
import re
from cogs.utils.chat_formatting import box, pagify, escape_mass_mentions
from random import choice
from copy import deepcopy

__author__ = "Danstr (and a little bit of plasma)"
__version__ = "0.2.a"

class BankError(Exception):
    pass
class NoAccount(BankError):
    pass

class Creditdrop:
    """A Red Cog to stimulate Nadeko's economy system."""

    def __init__(self, bot):
        self.bot = bot
        self.randNum = randint(95,102)
        self.number = (self.randNum)
        self.claimpot = 100
    #Admin Commands
    @commands.group(name="creditclaim", pass_context=True)
    async def creditclaim(self, ctx):
        """CreditClaim!"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @creditclaim.command(pass_context=True)
    @checks.admin_or_permissions(manage_server = True)
    async def setcredit(self, ctx, creditinput: int):
        """Set the number of credits that's given when claimed!"""
        self.claimpot = creditinput
        await self.bot.say('`[p]claim` amount now set to ' + str(self.claimpot) + ' credits!')

    #Claim Command
    @commands.command(pass_context = True)
    async def claim(self, ctx):
        """Credits, Credits, Credits! Get em while they're hot!"""

        claimauthor = ctx.message.author
        bank = self.bot.get_cog("Economy").bank
        if self.number == 100:
            try:
                await self.bot.say(str(claimauthor) + ' has gained ' + str(self.claimpot) + ' credits!')
                bank.deposit_credits(ctx.message.author, self.claimpot)
                self.randNum = randint(95, 102)

                self.number = (self.randNum)
            except Exception as e:
                print('Well, that broke. Heres why: {}'.format(type(e)))
        else:
            await self.bot.say("Money hasn't been dropped yet you beach bum!")
            self.randNum = randint(95, 102)
            self.number = (self.randNum)

    #Message Detector
    async def on_message(self, message):
        channel = message.channel
        author = message.author
        if author == self.bot.user:
            self.number = 500
        elif self.number == 100:
            print("Claim has been triggered!")
            claimmessage = 'Quick! ' + str(self.claimpot) + ' credits have been dropped on the boardwalk! Use `>claim` to get the money!'
            await self.bot.send_message(channel, claimmessage)
            await self.bot.wait_for_message(content = '>claim')
        else:
            self.randNum = randint(95, 102)
            self.number = (self.randNum)
            print(str(self.number))

def setup(bot):
    bot.add_cog(Creditdrop(bot))
