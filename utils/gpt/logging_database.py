import openai
import os
from dotenv import load_dotenv
import time
from logging_config import logger

load_dotenv()

openai.api_key = os.getenv("OPENAI_TOKEN")


def logging_database(query,origin):
    try:
       message = [
        {
        'role': 'user',
        'content': f'''
            Essa query:

            {query}
            Sera executada no meu banco de dados retorne para mim em apenas uma linha, qual mensagem de log deve ser salva após a execução dela. descreva o que foi feito de forma clara com apenas uma linha
        '''
        }
        ]   
       response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message
        )
        # Acessando o conteúdo da resposta corretamente
       response =  response.choices[0].message.content
       logger.info({"function" : origin, "message" : response})
    except Exception as e:
        logger.error(f"Erro ao criar mensagem: {e}")
        logger.warning({"function": origin,"message": "Query executada, mas não foi possivel alcançar OPENAI"})


    
    
