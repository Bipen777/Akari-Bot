import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def info(self, ctx):
        info_board = discord.Embed(
            title="Other Commands Akari Has for You!",
            description="Hai!",
            colour=discord.Colour.red()
        )
        info_board.set_footer(text="Akari")
        info_board.set_author(name="Bipen")
        info_board.add_field(name="akari", value="AKARI IS HERE!!!", inline=True)
        info_board.add_field(name="venti", value="Push him down the stairs!", inline=True)
        info_board.add_field(name="coinflip", value="Heads or Tails!", inline=True)
        info_board.add_field(name="avatar", value="Show Akari your Avatar!", inline=True)
        info_board.add_field(name="length", value="Show length of a document!", inline=True)
        await ctx.send(embed=info_board)

    @commands.command()
    async def avatar(self, ctx):
        await ctx.send(ctx.author.avatar_url)

    @commands.command()
    async def help(self, ctx):
        info_board = discord.Embed(
            title="Akari",
            colour=discord.Colour.orange()
        )
        info_board.set_footer(text="Akari")
        info_board.set_author(name="Bipen")
        info_board.add_field(name="akari match <ID>", value="Used to generate values for a match!", inline=False)
        info_board.add_field(name="akari schon", value="Toggle schedule reminders!", inline=False)
        await ctx.send(embed=info_board)


async def setup(bot):
    await bot.add_cog(Info(bot))
