from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # @commands.command()
    # async def wiki(self, ctx, msg):
    #     url: str = f"https://tr.wikipedia.org/wiki/{msg}"
    #     await ctx.send(f"Here : {url}")

    @commands.command()
    async def length(self, ctx, sent):
        sentence: str = ctx.message.content[7:]
        print(sentence)
        lenght: int = len(sentence)
        i = 0
        count: int = 0
        while i < lenght - 1:
            i += 1
            if sentence[i] == " ":
                count += 1
        word = count + 1
        letter = i + 1
        await ctx.send(f"World count : {word}, letter count : {letter}")

async def setup(bot):
    await bot.add_cog(Misc(bot))
