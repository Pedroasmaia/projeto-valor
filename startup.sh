echo "Instalando Dependencias"

pip freeze install -r requirements.txt

echo "Subindo Container"

sudo docker-compose up -d

echo "Rodando Aplicação"

python main.py