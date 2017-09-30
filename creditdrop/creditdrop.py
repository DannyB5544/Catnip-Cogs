import discord
from random import randint
from discord.ext import commands
from cogs.utils.dataIO import dataIO
import asyncio
from .utils import checks
import os
from __main__ import send_cmd_help
import os
import asyncio
import re
from cogs.utils.chat_formatting import box, pagify, escape_mass_mentions
from random import choice
# If I got here, congratulate myself for not fucking up yet.
__author__ = "Danstr"
__version__ = "0.0.3"

class CreditDrop:
    """CreditDrop. For those who want moar nadeko, apparently."""
    def __init__(self, bot):
        self.bot = bot
        self.randNum = randint(1, 10)
        self.number = (self.randNum)
        self.claimpot = 100
        
    @commands.group(name="creditdrop", pass_context=True)
    async def creditdrop(self, ctx):
        """CreditDrop!"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    @creditdrop.command(pass_context=True)
    @checks.is_owner()
    async def setcredit(self, ctx, creditinput: int):
        """Sets the credits a user will gain when  [p]claim is ran."""
        self.claimpot = creditinput
        await self.bot.say('[p]claim amount now set to ' + str(self.claimpot) + ' credits')
    # Put what your command does here
    # This command executes as !example poop
    @commands.command(pass_context=True)
    async def claim(self, ctx):

        """Credits! Get your Credits Right here!"""
        claimppi = ctx.message.author #Not sorry for that var name
        bank = self.bot.get_cog("Economy").bank #Finally grab the bank.
        if self.number == 7:
            await self.bot.say(claimppi + 'has gained ' + str(self.claimpot) + ' credits!')
            bank.deposit_credits(ctx.message.author, self.claimpot)
            self.randNum = randint(1, 10) # Re-rolls the number.
            self.number = (self.randNum)
        else:
            await self.bot.say('Lol no fuck off' + str(self.number))
            self.randNum = randint(1, 10) # Re-rolls the number.
            self.number = (self.randNum)
    async def on_message(self, ctx, message):
        channel = message.channel
        author = message.author
        self.randNum = randint(1, 10) # Re-rolls the number.
        self.number = (self.randNum)
        print(str(self.number))
        if self.number == 7: # LUCKY NUMBER 7! For testing only. When it goes live, there'll be a much higher count.
            await self.bot.send_message(channel=channel, content='The Magic number has been triggered! Quick! Use [p]claim to grab the credits! first one wins!')
        else:
            pass
def setup(bot):
    bot.add_cog(CreditDrop(bot))
