# Usando uma imagem Python base para o teste
FROM python:3.11-slim

# Definindo o diretório de trabalho no container
WORKDIR /app

# Copiando o script de teste e arquivos auxiliares para o container
COPY teste_exclusao_mutua.py /app/teste_exclusao_mutua.py
COPY utils.py /app/utils.py

# Instalando dependências necessárias
RUN pip install --no-cache-dir requests

# Comando para executar o teste automaticamente ao iniciar o container
CMD ["python", "teste_exclusao_mutua.py"]
