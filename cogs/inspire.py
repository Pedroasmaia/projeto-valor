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
            file_path = "cogs/frases.json"
            with open(file_path) as outfile:
                data = json.load(outfile)
                a = random.randint(0,len(data))                
                logger.info(f"Frase enviada: {data[a]}")
            await ctx.send(data[a])
        except FileNotFoundError:
            logger.error(f"Falha ao encontrar: {file_path}")
            await ctx.send("O comando solicitado não está disponível no momento.\nEstou constantemente aprendendo e me adaptando.\nPor favor, tente novamente mais tarde ou explore outras opções.")
        except Exception as e:
            logger.error(e)
            await ctx.send("O comando solicitado não está disponível no momento.\nEstou constantemente aprendendo e me adaptando.\nPor favor, tente novamente mais tarde ou explore outras opções.")
async def setup(bot):
    await bot.add_cog(Inspire(bot))
