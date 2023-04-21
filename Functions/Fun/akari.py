import random
from discord.ext import commands

class Akari(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def akari(self, ctx):
        await ctx.send("owo")

async def setup(bot):
    await bot.add_cog(Akari(bot))