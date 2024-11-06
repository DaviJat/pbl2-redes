# Usando uma imagem Python base
FROM python:3.11-slim

# Definindo o diretório de trabalho no container
WORKDIR /app

# Copiando os arquivos necessários para o container
COPY app.py /app/app.py
COPY utils.py /app/utils.py
COPY trechos_server_c.plk /app/trechos_server_c.plk
COPY requirements.txt /app/requirements.txt

# Instalando as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expondo a porta 5002 para o servidor Flask
EXPOSE 5002

# Comando para iniciar o servidor Flask
CMD ["python", "app.py"]

