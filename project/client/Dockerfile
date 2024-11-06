# Usando uma imagem Nginx para servir arquivos estáticos
FROM nginx:alpine

# Definindo o diretório de trabalho no container
WORKDIR /usr/share/nginx/html

# Removendo arquivos padrão do Nginx para evitar conflitos
RUN rm -rf ./*

# Copiando os arquivos do cliente para o diretório do Nginx
COPY index.html .
COPY styles.css .
COPY scripts.js .

# Expondo a porta 80 para o cliente
EXPOSE 80

