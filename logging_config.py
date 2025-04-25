import logging
from dotenv import load_dotenv
import os
from logging_loki import LokiHandler

load_dotenv()

handler = LokiHandler(
    url=os.getenv("URL_LOKI","http://localhost:3100/loki/api/v1/push"),  # URL do Loki
    tags={"application": "V.A.L.O.R"},  # Tags para identificar os logs
    version="1",  # Versão da API do Loki
)
formatter = logging.Formatter('%(levelname)s - %(message)s')


# Configuração do logger
logger = logging.getLogger("VALOR")
logger.setLevel(logging.INFO)  # Nível de log
handler.setFormatter(formatter)

# Adiciona o handler do Loki
logger.addHandler(handler)

