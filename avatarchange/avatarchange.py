import discord
import json
import os
import asyncio

from discord.ext import commands
from .utils.dataIO import dataIO

class LunaPics:
    """Automatically change bot profile picture"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.json_load('data/luna/settings.json')

    @commands.group()
    async def luna(self):
        """Luna pic's settings"""

        if not ctx.invoked_subcommand:
            await self.bot.send_cmd_help(ctx)

    def change(self):
        if self.settings['total'] < 2:
            pic = self.settings['1']
        else:
            picNum = randint(1, self.settings['total'])
            pic = self.settings[picNum]

        async with self.session.get(pic) as r:
                    data = await r.read()
        await self.bot.edit_profile(self.bot.settings.password, avatar=data)

        asyncio.sleep(300)

    @luna.command()
    async def add(self, url):
        """Add a pic"""

        if total not in self.settings:
            self.settings = {
                'total': 0
            }
        else:
            pass

        t = self.settings['total'] + 1

        if not url.endswith('.png')
            await self.bot.say("Invalid format. Please use `.png`")
            return
        else:
            self.settings[t] = url
            await self.bot.say("The picture  has been added")

    @luna.command()
    async def start(self):
        if 1 not in self.settings:
            return
        else:
            self.bot.loop.create_task(change())

def setup(bot):
    bot.add_cog(LunaPics(bot))

