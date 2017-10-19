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
from cogs.utils.dataIO import dataIOd
from random import randint
from random import choice

#Main Cogio
class Ship:
    #Defining Stuffios
    def __init__(self, bot):
        self.bot = bot
        self.firstSplit = []
        self.secondSplit = []
        self.listOfNames = []
        self.firstLength = 0
        self.secondLength = 0
        self.firstPart = 0
        self.secondPart = 0
        
    #Functionio
    def splitAndSort(name, whichPerson):
        prev = 0
        if whichPerson = 1:
            self.firstSplit.clear()
            while True:
                randomInt = random.randint(1, 3)
                self.firstSplit.append(name[prev:prev + randomInt])
                prev = prev + randomInt
                if prev >= len(name) - 1:
                    break
            self.firstLength = len(self.firstSplit) - 1

        elif whichPerson = 2:
            self.secondSplit.clear()
            while True:
                randomInt = random.randint(1, 3)
                self.secondSplit.append(name[prev:prev + randomInt])
                prev = prev + randomInt
                if prev >= len(name) - 1:
                    break
                self.secondLength = len(self.firstSplit) - 1

        else:
            print("The hell are you doing Plasma!")

    #The Commandio
    @commmands.command(pass_context = True)
    async def ship(self, ctx, user: discord.Member):
        """I'm not responsible for the horrible creations that may or may not come out of this cog! Enjoy!"""
        userName = str(user.Name)
        authorName = str(ctx.message.author.Name)

        splitAndSort(userName, 1)
        splitAndSort(authorName, 2)
        self.listOfNames.clear()

        x = 1
        while x <= 5:
            self.firstPart = random.randint(0, self.firstLength)
            self.secondPart = random.randint(0, self.secondLength)
            tempName = str(self.firstPart) + str(self.secondPart)
            self.listOfNames.append(tempName)
            x = x + 1

        shipNamesEmbed = discord.Embed(color = 0x95a5a6, description = "Ship Names!")

        x = 1
        while x <= 5:
            shipNamesEmbed.add_field(value = "#" + str(x) + ": " + str(self.listOfNames[x-1]))

        await self.bot.say(embed = shipNamesEmbed)

def setup(bot):
    bot.add_cog(Ship(bot))
