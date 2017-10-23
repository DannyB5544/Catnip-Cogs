#KITTENS! Oh wait, imports first.
import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
import time
import shutil
#Uh yeah, thats it. lol.

class httpcat:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def httpcat(self, num: int):
        """Randomly posts a http-cat from the
        aptly named httpcat site."""
        #And now for a lot of numbers. Agh.
        cats = ["100", "101", "200", "201", "202", "203", "204", "206",
        "207", "300", "301", "302", "303", "304", "305", "307", "400", "401",
        "402", "403", "404", "405", "406", "408", "409", "410", "411", "412",
        "414", "415", "416", "417", "418", "420", "421", "422", "423", "424",
        "425", "426", "429", "431", "444", "450", "500", "502", "503", "504",
        "506", "507", "508", "509", "511", "599"]
        if str(num) in cats:
            a = "https://http.cat/{}.jpg".format(str(num))
            await self.bot.say(a)
        else:
            ra = random.choice(cats)
            ra = "https://http.cat/{}.jpg".format(str(ra))
            await self.bot.say(ra)
def setup(bot):
    bot.add_cog(httpcat(bot))
