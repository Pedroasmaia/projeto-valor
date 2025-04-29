from discord.ext import commands
from logging_config import logger
from utils.gpt import perguntas
from database_config import runner_query

class GPT(commands.Cog):
    def __init__(self, bot): # Define o comportamento padrão da Classe
        self.bot = bot

    @commands.command()
    async def perguntar(self, ctx, * ,msg: str):
        logger.info("Executando comando $perguntar")
        try:
            discord_id = ctx.author.id
            logger.info(f"User: {discord_id}")
            response = perguntas.pergunta_command(msg)
            try:
                query = f'''
                SELECT qtd_perguntar FROM users WHERE id_discord == {discord_id}
                '''
                user = runner_query(query,'$perguntar')
                if user[0][0] == 0:
                    query = '''
                    INSERT INTO users (id_discord, name, qtd_perguntar)
                    VALUES (?, ?,?);
                    '''
                    values = (discord_id, ctx.author.name, 1)
                    try:
                        runner_query(query,'$perguntar',values)
                    except Exception as e:
                        logger.info(e)
                else:
                    logger.info(f"O Usuário {ctx.author.name} já rodou esse comando: {user[0][0] + 1}")
                    query = '''
                    UPDATE users
                    SET qtd_perguntar = ?
                    WHERE id_discord = ?
                    '''
                    values = (user[0][0]+1,discord_id)
                    try:
                        runner_query(query,'$perguntar',values)
                    except Exception as e:
                        logger.warning(f"Não foi possivel executar a query de atualização de valores: {e}")
            except Exception as e:
                logger.info(f"Não foi possivel executar a query de atualização: {e}")
            await ctx.send(response)
        except Exception as e:
            logger.warning(e)
            
async def setup(bot):
    await bot.add_cog(GPT(bot))
