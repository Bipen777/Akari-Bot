import discord
from discord.ext import commands, tasks

class Fun(commands.Cog):
    def __init__(self, bot):
        self.isYeet = 0
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def venti(self, ctx):
        if self.isYeet == 0:
            await ctx.send("Die Venti!")
            self.yeet.start(ctx)
            self.isYeet = 1
        else: 
            await ctx.send("No more die!")
            self.yeet.cancel()
            self.isYeet = 0

    @tasks.loop(seconds=60)
    async def yeet(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/503263475913457665/1008177540940181554/E4A6252D-7570-4729-8266-4CE2D9B71ED6.jpg")


async def setup(bot):
    await bot.add_cog(Fun(bot))
