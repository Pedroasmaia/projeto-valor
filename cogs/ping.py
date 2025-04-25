from discord.ext import commands
from logging_config import logger

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")
async def setup(bot):
    await bot.add_cog(Ping(bot))
