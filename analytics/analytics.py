#Imported Stuffios
import asyncio
import functools
import io
import os
import unicodedata
import aiohttp
import json
import random
import discord

from discord.ext import commands
from asyncio import sleep
from cogs.utils.dataIO import dataIO
from random import randint
from random import choice
from .utils import checks

class analytics:
    #Defining Stuffios
    def __init__(self, bot):
        self.bot = bot
        self.database_file = 'data/analytics/Database.json'
        self.database = dataIO.load_json(self.database_file)

    #Checkios
    async def save_database(self):
        dataIO.save_json(self.database_file, self.database)

    #Commands
    @commands.command(pass_context = True)
    async def messagecount(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        if not author.id in self.database[server.id]:
            message = "Looks like you've never sent any messages"
        else:
            message = "You've sent " + str(self.database[server.id][author.id]["Messages Sent"]) + " messages and " + str(self.database[server.id][author.id]["Characters Sent"]) + " characters!"

        await self.bot.say(message)

    #Message Dectectorio
    async def on_message(self, message):
        #Setupio Up Server
        server = message.server
        if server.id not in self.database:
            self.database[server.id] = {}

        #Word Count
        server = message.server
        author = message.author
        if not author.id in self.database[server.id]:
            self.database[server.id][author.id] = {}
            self.database[server.id][author.id]["Messages Sent"] = 0
            self.database[server.id][author.id]["Messages Sent"] += 1
            await self.save_database()
        else:
            self.database[server.id][author.id]["Messages Sent"] += 1
            await self.save_database()

        #Character Count
        messagelen = len(message.content)
        if not "Characters Sent" in self.database[server.id][author.id]:
            self.database[server.id][author.id]["Characters Sent"] = 0
            self.database[server.id][author.id]["Characters Sent"] += messagelen
            await self.save_database()
        else:
            self.database[server.id][author.id]["Characters Sent"] += messagelen
            await self.save_database()

#Check Folderio
def check_folder():
    if not os.path.exists("data/analytics"):
        print("Creating data/analytics folder...")
        os.makedirs("data/analytics")

#Check Fileio
def check_file():
    data = {}
    f = "data/analytics/Database.json"
    if not dataIO.is_valid_json(f):
        print("Creating default Database.json...")
        dataIO.save_json(f, data)

#Setupio
def setup(bot):
    check_folder()
    check_file()
    cog = analytics(bot)
    bot.add_cog(cog)
