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
from __main__ import send_cmd_help
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

    #Commandios
    @commands.command(pass_context = True)
    async def stats(self, ctx, user: discord.Member):
        """"Get stats on a person!"""
        server = ctx.message.server

        #Setupio
        if server.id not in self.database:
            self.database[server.id] = {}
        if user.id not in self.database[server.id]:
            self.database[server.id][user.id] = {}

        #Checkios
        if "rAdded" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["rAdded"] = 0
        if "mSent" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["mSent"] = 0
        if "cSent" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["cSent"] = 0
        if "mDeleted" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["mDeleted"] = 0
        if "ceSent" not in self.database[server.id][user.id]:
            self.database[server.id][user.id]["ceSent"] = 0

        statembed = discord.Embed(color = 0x546e7a)
        statembed.add_field(name = " ❯ Emote Stats", value = "Custom Emotes Sent: " + str(self.database[server.id][user.id]["ceSent"]) + "\n" + "Reactions Added: " + str(self.database[server.id][user.id]["rAdded"]), inline = False)
        statembed.add_field(name = " ❯ Message Stats", value = "Messages Sent: " + str(self.database[server.id][user.id]["mSent"]) + "\n" + "Characters Sent: " + str(self.database[server.id][user.id]["cSent"]) + "\n" + "Messages Deleted: " + str(self.database[server.id][user.id]["mDeleted"]), inline = False)
        await self.bot.send_message(ctx.message.channel, embed = statembed)

    @commands.command(pass_context = True)
    async def messagesdeleted(self, ctx):
        author = ctx.message.author
        server = ctx.message.server
        await self.bot.say("Messages Deleted: " + str(self.database[server.id][author.id]["mDeleted"]))

    #Sent Message Dectectorio
    async def on_message(self, message):
        #Setupio Up Server
        server = message.server
        if server.id not in self.database:
            self.database[server.id] = {}

        server = message.server
        author = message.author
        if not author.id in self.database[server.id]:
            self.database[server.id][author.id] = {}
            if "rAdded" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["rAdded"] = 0
            if "mSent" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["mSent"] = 0
            if "cSent" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["cSent"] = 0
            if "mDeleted" not in self.database[server.id][author.id]:
                self.database[server.id][author.id]["mDeleted"] = 0
            if "ceSent" not in self.database[server.id][author.id]:
                self.databse[server.id][author.id]["ceSent"] = 0
            self.database[server.id][author.id]["mSent"] = self.database[server.id][author.id]["mSent"] + 1
            await self.save_database()
        else:
            self.database[server.id][author.id]["mSent"] += 1
            await self.save_database()

        #Character Count
        messagelen = len(message.content)
        if not "cSent" in self.database[server.id][author.id]:
            self.database[server.id][author.id]["cSent"] = 0
            self.database[server.id][author.id]["cSent"] += messagelen
            await self.save_database()
        else:
            self.database[server.id][author.id]["cSent"] += messagelen
            await self.save_database()

        #Custom Emotes Count
        sentMessage = message.object
        splitMessages = sentMessage.split()
        emotesDetected = 0
        for temp in splitMessages:
            if temp[0] == "<":
                emotesDetected = emotesDetected + 1
            else:
                emotesDetected = emotesDetected

        if not "ceSent" in self.database[server.id][author.id]:
            self.database[server.id][author.id]["ceSent"] = 0
            self.database[server.id][author.id]["ceSent"] += emotesDetected
            await self.save_database()
        else:
            self.database[server.id][author.id]["ceSent"] += emotesDetected
            await self.save_database()

    #Deleted Message Dectectorio
    async def on_message_delete(self, message):
        server = message.server
        author = message.author
        if "mDeleted" not in self.database[server.id][author.id]:
            self.database[server.id][author.id]["mDeleted"] = 0
            self.database[server.id][author.id]["mDeleted"] = 1
            await self.save_database()
        else:
            self.database[server.id][author.id]["mDeleted"] += 1
            await self.save_database()

    #Reaction Detectionio
    # IDEA: Track most used emote
    async def on_reaction_add(self, reaction, user):
        server = user.server
        author = user
        if "rAdded" not in self.database[server.id][author.id]:
            self.database[server.id][author.id]["rAdded"] = 0
            self.database[server.id][author.id]["rAdded"] += 1
            await self.save_database()
        else:
            self.database[server.id][author.id]["rAdded"] = self.database[server.id][author.id]["rAdded"] + 1
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
