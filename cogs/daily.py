from discord.ext import commands
from logging_config import logger
from database_config import runner_query
import random

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self, ctx, * ,msg: str,name="$daily"):
        incentive_phrases = [
    "Sua mensagem foi registrada: Cada passo conta, mantenha o foco no seu caminho.",
    "Sua mensagem foi registrada: O progresso está nas pequenas ações diárias. Continue assim!",
    "Sua mensagem foi registrada: A resiliência é o que fortalece sua jornada. Vamos juntos!",
    "Sua mensagem foi registrada: Organize-se, o sucesso vem com foco. Continue em frente!",
    "Sua mensagem foi registrada: Liderança se constrói com ações consistentes. Você está no caminho certo!",
    "Sua mensagem foi registrada: A cada desafio, você cresce mais. Não pare agora!",
    "Sua mensagem foi registrada: Foco no objetivo. Estamos cada vez mais perto do sucesso!",
    "Sua mensagem foi registrada: A jornada é longa, mas sua determinação vai te levar longe."
]
        author = ctx.author.mention
        if ctx.guild is None:
            if len(msg) <= 501:
                try:
                    id_valor = runner_query("SELECT id_valor FROM users WHERE id_discord = ?",name,values=(ctx.author.id,))
                    if id_valor:
                        query = '''
                        INSERT INTO daily (user_id, daily_text)
                        VALUES (?, ?);
                        '''
                        id_valor = id_valor[0][0]
                        values = (id_valor,msg,)
                        try:
                            runner_query(query,name,values)            
                            await ctx.author.send(f'{random.choice(incentive_phrases)}')
                        except Exception as e:
                            logger.warning(e)
                    else:
                        query = '''
                        INSERT INTO users (id_discord, name, qtd_perguntar)
                        VALUES (?, ?,?);
                        '''
                        values = (ctx.author.id, ctx.author.name, 1)
                        try:
                            runner_query(query,name,values)
                        except Exception as e:
                            logger.info(e)
                    
                except Exception as e:
                    logger.warning(f"Não foi possivel enviar mensagem no privado: {e}")
                    await ctx.send(f"{ctx.author.mention}, não consegui te mandar uma DM. Verifique suas configurações de privacidade.")
            else:
                logger.info("Usuário tentou enviar mais de 500 caracteres")
                await ctx.author.send(f'{author}, por favor mantenha a mensagem com menos de 500 caracteres')
        else:
            logger.info(f'Comando foi chamado a partir de um canal publico: {ctx.guild}')
            try:
                await ctx.message.delete()
                await ctx.author.send(f'{author}, você usou o comando Daily em um canal publico, use apenas no chat privado')
                logger.info('Mensagem excluida')
            except Exception as e:
                logger.warning(f"Falha: {e}")
        
async def setup(bot):   
    await bot.add_cog(Daily(bot))