from discord.ext import commands
from logging_config import logger
import json
import random

class Inspire(commands.Cog):
    def __init__(self, bot): # Define o comportamento padrão da Classe
        self.bot = bot


    @commands.command()
    async def frase(self, ctx):
        logger.info("Executando novo comando")
        try:
            with open("cogs/frases.json") as outfile:
                data = json.load(outfile)
                a = random.randint(0,len(data))                
                logger.warning("O Usuário pediu uma frase")
            await ctx.send(data[a])
        except Exception as e:
            logger.warning(e)
async def setup(bot):
    await bot.add_cog(Inspire(bot))
