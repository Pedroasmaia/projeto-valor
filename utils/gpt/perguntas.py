import openai
import os
from dotenv import load_dotenv
import time
from logging_config import logger

load_dotenv()

openai.api_key = os.getenv("OPENAI_TOKEN")


def pergunta_command(msg: str) -> str:
    # 1. Cria uma nova thread
    try:
        logger.info("Criando Thread")
        thread = openai.beta.threads.create()

        # 2. Adiciona a mensagem do usuário na thread
        try:
            openai.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=msg
            )

            # 3. Executa o assistant
            try:
                run = openai.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=os.getenv("VALOR_ASSISTANTS_ID")
                )
            # 4. Esperar o run terminar (simplificado com polling)
                import time

                while True:
                    run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                    if run_status.status == "completed":
                        break
                    time.sleep(1)

                messages = openai.beta.threads.messages.list(
                        thread_id=thread.id,
                        order="desc",  # mensagens mais recentes primeiro
                        limit=5        # só as últimas, pra ser rápido
                    )
                for message in messages.data:
                    if message.run_id == run.id and message.role == "assistant":
                        return message.content[0].text.value
            except Exception as e:
                    logger.error(f"Erro ao recuperar mensagem: {e}")

        except Exception as e:
            logger.error(f"Falha ao adicionar mensagem a conversa: {e}")

    except Exception as e:
        logger.error(f"Erro ao criar thread: {e}")


    
    
