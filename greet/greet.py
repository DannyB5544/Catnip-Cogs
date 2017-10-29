# Note- Based on IR's Welcome
# Import- Modules
import discord
import asyncio
import os

from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import pagify
from __main__ import send_cmd_help
from copy import deepcopy

# Default- Settings
default_settings = {'Greeting': "Welcome {0.name} to {1.name}!", 'On': False, 'Channel': None}
settings_path = "data/greet/settings.json"

# Class- Greet
class Greet:
    # Define- Variables
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(settings_path)
        self.timeTracker = {}

    # Function- Save settings
    async def save_settings(self):
        dataIO.save_json(settings_path, self.settings)

    # Command Group- Settings
    @commands.group(pass_context = True)
    @checks.admin_or_permissions(manage_server = True)
    async def greetset(self, ctx):
        """Sets greet module settings"""

        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = deepcopy(default_settings)
            self.settings[server.id]['Channel'] = server.default_channel.id
            dataIO.save_json(settings_path, self.settings)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    # Command- Set greeting
    @greetset.command(pass_context = True)
    async def msg(self, ctx, *, greetMessage: str):
        """Change your welcome message!

        {0} is user
        {1} is server
        Default is set to:
            Welcome {0.name} to {1.name}!

        Example formats:
            {0.mention}.. What are you doing here?
            {1.name} has a new member! {0.name}#{0.discriminator} - {0.id}
            Someone new joined! Who is it?! D: IS HE HERE TO HURT US?!"""

        server = ctx.message.server
        self.settings[server.id]['Greeting'] = greetMessage
        await self.save_settings()
        await self.bot.say("Greeting message added for the server!")

    # Command- Toggle
    @greetset.command(pass_context = True)
    async def toggle(self, ctx):
        """Turns greeting off and on!"""

        server = ctx.message.server
        self.settings[server.id]['On'] = not self.settings[server.id]['On']
        if self.settings[server.id]['On']:
            await self.bot.say("I will now welcome new users to the server.")
        else:
            await self.bot.say("I will no longer welcome new users.")
        await self.save_settings()

    # Command- ChannelType
    @greetset.command(pass_context = True)
    async def channel(self, ctx, greetChannel: discord.Channel = None):
        """Set the greeting channel!"""

        server = ctx.message.server
        if greetChannel == None:
            greetChannel = ctx.message.server.default_channel
        if not server.get_member(self.bot.user.id).permissions_in(channel).send_messages:
            await self.bot.say("I do not have permissions to send messages to {0.mention}".format(channel))
            return
        self.settings[server.id]['Channel'] = greetChannel.id
        await self.save_settings()

    # Detection- Member joined
    async def member_join(self, member):
        server = member.server
        if server.id not in self.settings:
            self.settings[server.id] = deepcopy(default_settings)
            self.settings[server.id]['Channel'] = server.default_channel.id
            dataIO.save_json(settings_path, self.settings)
        if not self.settings[server.id]['On']:
            return

        channel = self.get_welcome_channel(server)
        msg = str(self.get_welcome_message(server))

        if channel is None:
            print('Greet.py: Channel not found. It was most likely deleted. User joined: {}'.format(member.name))
        else:
            greetEmbed = discord.Embd(color = 0xA9DFBF)
            greetEmbed.add_field(name = "", value = msg.format(member, server))
            await self.bot.send_message(channel, embed = greetEmbed)
            self.add_to_tracker(member)

    # Detection- Member left
    async def member_leave(self, member):
        server = member.server
        if not self.settings[server.id]['On']:
            return

        seconds = abs(self.timeTracker[member.id] - int(time.perf_counter()))
        channel = self.get_welcome_channel(server)
        msg = "Sorry to see you go so soon, "

        if channel is None:
            print('Greet.py: Channel not found. It was most likely deleted. User joined: {}'.format(member.name))
        elif seconds > 5:
            print('Greet.py: Passed time limit. User left: {}'.format(member.name))
            self.remove_from_tracker(member)
        else:
            leaveEmbed = discord.Embd(color = 0xF1948A)
            leaveEmbed.add_field(name = "", value = msg + str(member.name) + "!")
            await self.bot.send_message(channel, embed = leaveEmbed)
            self.remove_from_tracker(member)

    # Function- Add to timer
    def add_to_tracker(self, member):
        try:
            self.timeTracker[member.id] = int(time.perf_counter())
        except:
            return None

    # Function- Remove from timer
    def remove_from_tracker(self, member):
        try:
            del self.timeTracker[member.id]
        except:
            return None

    # Function- Get greet channel
    def get_welcome_channel(self, server):
        try:
            return server.get_channel(self.settings[server.id]['Channel'])
        except:
            return None

    # Function- Get greet message
    def get_welcome_message(self, server):
        try:
            return self.settings[server.id]['Greeting']
        except:
            return None

    # Function- Get greet toggle
    def get_welcome_toggle(self, server):
        try:
            return self.settings[server.id]['On']
        except:
            return None

# Check - Folder existence
def check_folders():
    if not os.path.exists("data/greet"):
        print("Creating data/greet folder...")
        os.makedirs("data/greet")

# Check - File existence
def check_files():
    f = settings_path
    if not dataIO.is_valid_json(f):
        print("Creating greet settings.json...")
        dataIO.save_json(f, {})
    else:  # consistency check
        current = dataIO.load_json(f)
        for k, v in current.items():
            if v.keys() != default_settings.keys():
                for key in default_settings.keys():
                    if key not in v.keys():
                        current[k][key] = deepcopy(default_settings)[key]
                        print("Adding " + str(key) +
                              " field to welcome settings.json")
        # upgrade. Before GREETING was 1 string
        for server in current.values():
            if isinstance(server['Greeting'], str):
                server['Greeting'] = [server['Greeting']]
        dataIO.save_json(f, current)

# Setup - Cog
def setup(bot):
    check_folders()
    check_files()
    n = Greet(bot)
    bot.add_listener(n.member_join, "on_member_join")
    bot.add_cog(n)
