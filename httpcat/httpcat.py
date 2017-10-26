#KITTENS! Oh wait, imports first.
import discord
from discord.ext import commands
import asyncio
import aiohttp
from random import randint
import time
import shutil
#Uh yeah, thats it. lol.

class httpcat:
    def __init__(self, bot):
        self.bot = bot
        self.cats = ["100", "101", "200", "201", "202", "203", "204", "206",
                     "207", "300", "301", "302", "303", "304", "305", "307", "400", "401",
                     "402", "403", "404", "405", "406", "408", "409", "410", "411", "412",
                     "414", "415", "416", "417", "418", "420", "421", "422", "423", "424",
                     "425", "426", "429", "431", "444", "450", "500", "502", "503", "504",
                     "506", "507", "508", "509", "511", "599"]
    
    @commands.command(pass_context=True)
    async def httpcat(self, ctx, num: int = None):
        """Randomly posts a http-cat from the
            aptly named httpcat site."""
        
        if num is None:
            rand = randint(0, len(self.cats)-1)
            message = "https://http.cat/{}.jpg".format(self.cats[rand])
        
        elif str(num) not in self.cats:
            message = "Cat not found\nhttps://http.cat/404.jpg"
        
        else:
            for cat in self.cats:
                if cat == str(num):
                    message = "https://http.cat/{}.jpg".format(str(num))
                    break
        
        await self.bot.say(message)

def setup(bot):
    bot.add_cog(httpcat(bot))
