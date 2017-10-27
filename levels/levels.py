# Imports
import discord
import os
import time

from discord.ext import commands
from .utils import checks
from .utils.dataIO import dataIO
from __main__ import send_cmd_help
from random import randint


class levels:
    """This is Riding's old level cog with my improvements!"""
    def __init__(self, bot):
        self.bot = bot
        self.userDefaults = {"XP": 0, "Level": 0}
        self.database_file = 'data/levels/Database.json'
        self.database = dataIO.load_json(self.database_file)
        self.xpCounter = {}

        # Function - Save database
        async def save_database(self):
            dataIO.save_json(self.database_file, self.database)

        # Command - Register everyone
        @commands.command(pass_context=True)
        async def allreg(self, ctx):
            """Register all members to the database!"""
            server = ctx.message.server
            registerCount = 0
            register_server(server.id)

            for m in server.members:
                if m.id not in self.database[server.id]:
                    registerCount += 1
                    register_person(server.id, m.id)
            await self.bot.say("Registering Done! I've registered " + str(registerCount) + " members!")

        # Command - Check rank
        @commands.command(name="show", pass_context=True)
        async def rank(self, ctx, user : discord.Member=None):
            server = ctx.message.server
            if not user:
                user = ctx.message.author
            if self.check_joined(user.id):
                embed = discord.Embed(color=0x546e7a)
                embed.add_field(name="Rank!",value="Level: {} \nXP: {}/{}".format(self.get_level(server.id, user.id), self.get_xp(server.id, author.id), self.get_level_xp(self.database[server.id][user.id]["XP"])))
            else:
                embed = discord.Embed(color=0xe74c3c)
                embed.add_field(name="Error!",value="There was an error getting the stats!")

            await self.bot.send_message(ctx.message.channel, embed=embed)

        # Message Event - Handles XP
        async def on_message(self, ctx, message):
            server = message.server
            author = message.author

            register_server(server.id)
            embed = discord.Embed(color=0x546e7a)

            if self.check_joined(server.id, author.id):
                if author.id in self.xpCounter:
                    seconds = abs(self.xpCounter[author.id] - int(time.perf_counter()))
                    if seconds > 60:
                         self.add_xp(server.id, author.id)
                         self.xpCounter[author.id] = int(time.perf_counter())
                         await self.save_database
                    if self.need_level_up(server.id, author.id):
                        self.level_up(server.id, author.id)
                        message = "Whoo! {} has ascended to level {}".format(author.display_name, self.database[server.id][author.id]["Level"])
                        embed.add_field(name="Level Up!", value=message)
                        await self.bot.send_message(ctx.message.channel, embed = embed)
            else:
                self.register_person(server.id, author.id)
                self.add_xp(server.id, author.id)
                self.xpCounter[author.id] = int(time.perf_counter())
                await save_database()


        # Function - Check if user is in database
        def check_joined(self, sid, mid):
            if mid in self.database[sid]:
                return True
            else:
                return False

        # Funtion - Add XP
        def add_xp(self, sid, mid):
            if self.check_joined(self, sid, mid):
                self.database[sid][mid]["XP"] += int(randint(15, 20))
                await self.save_database()

        # Function - Get XP needed to level up
        def get_level_xp(self, level):
            xpneed = 5*(int(level)**2)+50*int(level)+100
            return xpneed

        # Function - Get user level
        def get_level(self, sid, mid):
            if self.check_joined(sid, mid):
                return self.database[sid][mid]["Level"]

        # Function - Get user XP
        def get_xp(self, sid, mid):
            if self.check_joined(sid, mid):
                return self.database[sid][mid]["XP"]

        # Function - Level them up
        def level_up(self, sid, mid):
            self.database[sid][mid]["Level"] += 1
            self.database[sid][mid]["XP"] = 0
            await self.save_database()

        # Function - Check if they need to level up
        def need_level_up(self, sid, mid):
            if self.database[sid][mid]["XP"] > self.get_level_xp(self.database[sid][mid]["Level"]):
                return True
            else:
                return False

        # Function - Registers user
        def register_person(self, sid, mid):
            self.database[sid][mid] = self.userDefaults
            await self.save_database()

        # Function - Registers server
        def register_server(self, sid):
            if sid not in self.database:
                self.database[sid] = {}
                await self.save_database()

# Function - Check folder existence
def check_folder():
    if not os.path.exists("data/levels"):
        print("Creating data/levels folder...")
        os.makedirs("data/levels")

# Function - Check file existence
def check_file():
    data = {}
    f = "data/levels/Database.json"
    if not dataIO.is_valid_json(f):
        print("Creating default Database.json...")
        dataIO.save_json(f, data)

#Setupio
def setup(bot):
    check_folder()
    check_file()
    cog = levels(bot)
    bot.add_cog(cog)
