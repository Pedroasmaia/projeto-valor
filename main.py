import os
import discord
from discord.ext import commands
from dotenv import load_dotenv  # opcional, se estiver usando .env
import asyncio
from logging_config import logger

# Carrega variáveis de ambiente (caso use .env)
load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Cria o bot
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user}")

# Setup assíncrono
async def setup():
    logger.info("Carregando Cogs...")
    await bot.load_extension("cogs.ping")  # aqui você carrega todos os cogs
    await bot.load_extension("cogs.inspire")
    logger.info("Iniciando bot VALOR...")
    await bot.start(os.getenv("DISCORD_TOKEN"))

# Executa o setup assíncrono
if __name__ == "__main__":
    asyncio.run(setup())
