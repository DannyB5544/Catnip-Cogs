#Imported Stuffios
import asyncio
import functools
import io
import os
import unicodedata
import aiohttp
import json

from discord.ext import commands
from asyncio import sleep
from cogs.utils.dataIO import dataIO

#Main Cog
class EmojiChat:
    #Defining Stuffios
    def __init__(self, bot):
        self.bot = bot
        self.isECOn = False
        self.placeHolder = True
        self.unicodeTrue = False
        self.replacementCharacters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    #The Commandio
    @commands.command(pass_context = True)
    async def ec(self, ctx, timeOn: int ):
        """Emoji Chat Toggle!"""
        if self.isECOn == True:
            await self.bot.say("Emoji Chat is already on.")

        user = ctx.message.author
        bank = self.bot.get_cog("Economy").bank
        totalCredits = bank.get_balance(user)

        if totalCredits > timeOn * 500:
            creditsToWithdraw = timeOn * 500
            await self.bot.say("Emoji Chat is on for " + str(timeOn) + " minutes!")
            self.isECOn = True
            bank.withdraw_credits(user, creditsToWithdraw)
            await asyncio.sleep(60 * timeOn)
            self.isECOn = False
            await self.bot.say("Emoji Chat is off!")

        else:
            creditsNeeded = (timeOn * 500) - totalCredits
            await self.bot.say("You're short " + str(creditsNeeded) + " credits.")


    #Message Detectionio
    async def on_message(self, message):
        if message.content == "PleaseEndMySufferingPlasma":
            self.isECOn = False

        if self.isECOn == True:
            splitMessage = sentMessage.split()

            for temp in splitMessage:
                #This is FlapJack's Emote Check Code modified by Me
                emoji = list(str(temp))
                if emoji[0] == '<':
                    self.unicodeTrue = False
                    try:
                        name = temp.split(':')[1]
                    except:
                        await self.bot.delete_message(message)
                else:
                    await self.bot.delete_message(message)
                            
        else:

def setup(bot):
    bot.add_cog(EmojiChat(bot))
