import random

from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def giveaway(self, ctx):
        """
        Picks a random user from the server to win your giveaway.
        """
        await ctx.send(f"Winner: {random.choice(ctx.guild.members).mention}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
