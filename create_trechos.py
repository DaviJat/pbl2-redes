import pickle
import os

trechos_a = [
    {"id": 1, "servidor": "a", "origem": "São Paulo", "destino": "Rio de Janeiro", "distancia": 430, "quantidade_passagens": 100},
    {"id": 2, "servidor": "a", "origem": "São Paulo", "destino": "Brasília", "distancia": 1015, "quantidade_passagens": 100},
    {"id": 3, "servidor": "a", "origem": "São Paulo", "destino": "Salvador", "distancia": 1960, "quantidade_passagens": 100},
    {"id": 4, "servidor": "a", "origem": "São Paulo", "destino": "Fortaleza", "distancia": 3120, "quantidade_passagens": 100},
    {"id": 5, "servidor": "a", "origem": "São Paulo", "destino": "Belo Horizonte", "distancia": 585, "quantidade_passagens": 100},
    {"id": 6, "servidor": "a", "origem": "São Paulo", "destino": "Manaus", "distancia": 3930, "quantidade_passagens": 100},
    {"id": 7, "servidor": "a", "origem": "São Paulo", "destino": "Curitiba", "distancia": 410, "quantidade_passagens": 100},
    {"id": 8, "servidor": "a", "origem": "São Paulo", "destino": "Recife", "distancia": 2670, "quantidade_passagens": 100},
    {"id": 9, "servidor": "a", "origem": "São Paulo", "destino": "Porto Alegre", "distancia": 1115, "quantidade_passagens": 100},
    {"id": 10, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Brasília", "distancia": 1160, "quantidade_passagens": 100},
    {"id": 11, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Salvador", "distancia": 1660, "quantidade_passagens": 100},
    {"id": 12, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Fortaleza", "distancia": 2800, "quantidade_passagens": 100},
    {"id": 13, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Belo Horizonte", "distancia": 440, "quantidade_passagens": 100},
    {"id": 14, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Manaus", "distancia": 3680, "quantidade_passagens": 100},
    {"id": 15, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Curitiba", "distancia": 850, "quantidade_passagens": 100},
    {"id": 16, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Recife", "distancia": 2330, "quantidade_passagens": 100},
    {"id": 17, "servidor": "a", "origem": "Rio de Janeiro", "destino": "São Paulo", "distancia": 430, "quantidade_passagens": 100},
    {"id": 18, "servidor": "a", "origem": "Brasília", "destino": "São Paulo", "distancia": 1015, "quantidade_passagens": 100},
    {"id": 19, "servidor": "a", "origem": "Salvador", "destino": "São Paulo", "distancia": 1960, "quantidade_passagens": 100},
    {"id": 20, "servidor": "a", "origem": "Fortaleza", "destino": "São Paulo", "distancia": 3120, "quantidade_passagens": 100},
    {"id": 21, "servidor": "a", "origem": "Belo Horizonte", "destino": "São Paulo", "distancia": 585, "quantidade_passagens": 100},
    {"id": 22, "servidor": "a", "origem": "Manaus", "destino": "São Paulo", "distancia": 3930, "quantidade_passagens": 100},
    {"id": 23, "servidor": "a", "origem": "Curitiba", "destino": "São Paulo", "distancia": 410, "quantidade_passagens": 100},
    {"id": 24, "servidor": "a", "origem": "Recife", "destino": "São Paulo", "distancia": 2670, "quantidade_passagens": 100},
    {"id": 25, "servidor": "a", "origem": "Porto Alegre", "destino": "São Paulo", "distancia": 1115, "quantidade_passagens": 100},
    {"id": 26, "servidor": "a", "origem": "Brasília", "destino": "Rio de Janeiro", "distancia": 1160, "quantidade_passagens": 100},
    {"id": 27, "servidor": "a", "origem": "Salvador", "destino": "Rio de Janeiro", "distancia": 1660, "quantidade_passagens": 100},
    {"id": 28, "servidor": "a", "origem": "Fortaleza", "destino": "Rio de Janeiro", "distancia": 2800, "quantidade_passagens": 100},
    {"id": 29, "servidor": "a", "origem": "Belo Horizonte", "destino": "Rio de Janeiro", "distancia": 440, "quantidade_passagens": 100},
    {"id": 30, "servidor": "a", "origem": "Manaus", "destino": "Rio de Janeiro", "distancia": 3680, "quantidade_passagens": 100},
    {"id": 31, "servidor": "a", "origem": "Curitiba", "destino": "Rio de Janeiro", "distancia": 850, "quantidade_passagens": 100},
    {"id": 32, "servidor": "a", "origem": "Recife", "destino": "Rio de Janeiro", "distancia": 2330, "quantidade_passagens": 100}
]

trechos_b = [
    {"id": 1, "servidor": "b", "origem": "Rio de Janeiro", "destino": "Porto Alegre", "distancia": 1550, "quantidade_passagens": 100},
    {"id": 2, "servidor": "b", "origem": "Brasília", "destino": "Salvador", "distancia": 1440, "quantidade_passagens": 100},
    {"id": 3, "servidor": "b", "origem": "Brasília", "destino": "Fortaleza", "distancia": 2200, "quantidade_passagens": 100},
    {"id": 4, "servidor": "b", "origem": "Brasília", "destino": "Belo Horizonte", "distancia": 740, "quantidade_passagens": 100},
    {"id": 5, "servidor": "b", "origem": "Brasília", "destino": "Manaus", "distancia": 3490, "quantidade_passagens": 100},
    {"id": 6, "servidor": "b", "origem": "Brasília", "destino": "Curitiba", "distancia": 1370, "quantidade_passagens": 100},
    {"id": 7, "servidor": "b", "origem": "Brasília", "destino": "Recife", "distancia": 2200, "quantidade_passagens": 100},
    {"id": 8, "servidor": "b", "origem": "Brasília", "destino": "Porto Alegre", "distancia": 2020, "quantidade_passagens": 100},
    {"id": 9, "servidor": "b", "origem": "Salvador", "destino": "Fortaleza", "distancia": 1020, "quantidade_passagens": 100},
    {"id": 10, "servidor": "b", "origem": "Salvador", "destino": "Belo Horizonte", "distancia": 1370, "quantidade_passagens": 100},
    {"id": 11, "servidor": "b", "origem": "Salvador", "destino": "Manaus", "distancia": 4430, "quantidade_passagens": 100},
    {"id": 12, "servidor": "b", "origem": "Salvador", "destino": "Curitiba", "distancia": 2290, "quantidade_passagens": 100},
    {"id": 13, "servidor": "b", "origem": "Salvador", "destino": "Recife", "distancia": 800, "quantidade_passagens": 100},
    {"id": 14, "servidor": "b", "origem": "Salvador", "destino": "Porto Alegre", "distancia": 3070, "quantidade_passagens": 100},
    {"id": 15, "servidor": "b", "origem": "Fortaleza", "destino": "Belo Horizonte", "distancia": 2520, "quantidade_passagens": 100},
    {"id": 16, "servidor": "b", "origem": "Fortaleza", "destino": "Manaus", "distancia": 5680, "quantidade_passagens": 100},
    {"id": 17, "servidor": "b", "origem": "Porto Alegre", "destino": "Rio de Janeiro", "distancia": 1550, "quantidade_passagens": 100},
    {"id": 18, "servidor": "b", "origem": "Salvador", "destino": "Brasília", "distancia": 1440, "quantidade_passagens": 100},
    {"id": 19, "servidor": "b", "origem": "Fortaleza", "destino": "Brasília", "distancia": 2200, "quantidade_passagens": 100},
    {"id": 20, "servidor": "b", "origem": "Belo Horizonte", "destino": "Brasília", "distancia": 740, "quantidade_passagens": 100},
    {"id": 21, "servidor": "b", "origem": "Manaus", "destino": "Brasília", "distancia": 3490, "quantidade_passagens": 100},
    {"id": 22, "servidor": "b", "origem": "Curitiba", "destino": "Brasília", "distancia": 1370, "quantidade_passagens": 100},
    {"id": 23, "servidor": "b", "origem": "Recife", "destino": "Brasília", "distancia": 2200, "quantidade_passagens": 100},
    {"id": 24, "servidor": "b", "origem": "Porto Alegre", "destino": "Brasília", "distancia": 2020, "quantidade_passagens": 100},
    {"id": 25, "servidor": "b", "origem": "Fortaleza", "destino": "Salvador", "distancia": 1020, "quantidade_passagens": 100},
    {"id": 26, "servidor": "b", "origem": "Belo Horizonte", "destino": "Salvador", "distancia": 1370, "quantidade_passagens": 100},
    {"id": 27, "servidor": "b", "origem": "Manaus", "destino": "Salvador", "distancia": 4430, "quantidade_passagens": 100},
    {"id": 28, "servidor": "b", "origem": "Curitiba", "destino": "Salvador", "distancia": 2290, "quantidade_passagens": 100},
    {"id": 29, "servidor": "b", "origem": "Recife", "destino": "Salvador", "distancia": 800, "quantidade_passagens": 100},
    {"id": 30, "servidor": "b", "origem": "Porto Alegre", "destino": "Salvador", "distancia": 3070, "quantidade_passagens": 100},
    {"id": 31, "servidor": "b", "origem": "Belo Horizonte", "destino": "Fortaleza", "distancia": 2520, "quantidade_passagens": 100},
    {"id": 32, "servidor": "b", "origem": "Manaus", "destino": "Fortaleza", "distancia": 5680, "quantidade_passagens": 100}
]


trechos_c = [
    {"id": 1, "servidor": "c", "origem": "Fortaleza", "destino": "Curitiba", "distancia": 3680, "quantidade_passagens": 100},
    {"id": 2, "servidor": "c", "origem": "Fortaleza", "destino": "Recife", "distancia": 800, "quantidade_passagens": 100},
    {"id": 3, "servidor": "c", "origem": "Fortaleza", "destino": "Porto Alegre", "distancia": 4570, "quantidade_passagens": 100},
    {"id": 4, "servidor": "c", "origem": "Belo Horizonte", "destino": "Manaus", "distancia": 3930, "quantidade_passagens": 100},
    {"id": 5, "servidor": "c", "origem": "Belo Horizonte", "destino": "Curitiba", "distancia": 1000, "quantidade_passagens": 100},
    {"id": 6, "servidor": "c", "origem": "Belo Horizonte", "destino": "Recife", "distancia": 2090, "quantidade_passagens": 100},
    {"id": 7, "servidor": "c", "origem": "Belo Horizonte", "destino": "Porto Alegre", "distancia": 1710, "quantidade_passagens": 100},
    {"id": 8, "servidor": "c", "origem": "Manaus", "destino": "Curitiba", "distancia": 4360, "quantidade_passagens": 100},
    {"id": 9, "servidor": "c", "origem": "Manaus", "destino": "Recife", "distancia": 5900, "quantidade_passagens": 100},
    {"id": 10, "servidor": "c", "origem": "Manaus", "destino": "Porto Alegre", "distancia": 4900, "quantidade_passagens": 100},
    {"id": 11, "servidor": "c", "origem": "Curitiba", "destino": "Recife", "distancia": 3030, "quantidade_passagens": 100},
    {"id": 12, "servidor": "c", "origem": "Curitiba", "destino": "Porto Alegre", "distancia": 710, "quantidade_passagens": 100},
    {"id": 13, "servidor": "c", "origem": "Recife", "destino": "Porto Alegre", "distancia": 3700, "quantidade_passagens": 100},
    {"id": 14, "servidor": "c", "origem": "Curitiba", "destino": "Fortaleza", "distancia": 3680, "quantidade_passagens": 100},
    {"id": 15, "servidor": "c", "origem": "Recife", "destino": "Fortaleza", "distancia": 800, "quantidade_passagens": 100},
    {"id": 16, "servidor": "c", "origem": "Porto Alegre", "destino": "Fortaleza", "distancia": 4570, "quantidade_passagens": 100},
    {"id": 17, "servidor": "c", "origem": "Manaus", "destino": "Belo Horizonte", "distancia": 3930, "quantidade_passagens": 100},
    {"id": 18, "servidor": "c", "origem": "Curitiba", "destino": "Belo Horizonte", "distancia": 1000, "quantidade_passagens": 100},
    {"id": 19, "servidor": "c", "origem": "Recife", "destino": "Belo Horizonte", "distancia": 2090, "quantidade_passagens": 100},
    {"id": 20, "servidor": "c", "origem": "Porto Alegre", "destino": "Belo Horizonte", "distancia": 1710, "quantidade_passagens": 100},
    {"id": 21, "servidor": "c", "origem": "Curitiba", "destino": "Manaus", "distancia": 4360, "quantidade_passagens": 100},
    {"id": 22, "servidor": "c", "origem": "Recife", "destino": "Manaus", "distancia": 5900, "quantidade_passagens": 100},
    {"id": 23, "servidor": "c", "origem": "Porto Alegre", "destino": "Manaus", "distancia": 4900, "quantidade_passagens": 100},
    {"id": 24, "servidor": "c", "origem": "Recife", "destino": "Curitiba", "distancia": 3030, "quantidade_passagens": 100},
    {"id": 25, "servidor": "c", "origem": "Porto Alegre", "destino": "Curitiba", "distancia": 710, "quantidade_passagens": 100},
    {"id": 26, "servidor": "c", "origem": "Porto Alegre", "destino": "Recife", "distancia": 3700, "quantidade_passagens": 100}
]

base_diretorio = "project"

diretorios = {
    "server_a": trechos_a,
    "server_b": trechos_b,
    "server_c": trechos_c
}

# Criar pastas e salvar arquivos
for nome_diretorio, dados_trechos in diretorios.items():
    # Caminho completo da pasta
    caminho_diretorio = os.path.join(base_diretorio, nome_diretorio)

    # Cria o diretório se ele não existir
    os.makedirs(caminho_diretorio, exist_ok=True)

    # Caminho completo do arquivo dentro da pasta
    caminho_arquivo = os.path.join(caminho_diretorio, f"trechos_{nome_diretorio}.plk")

    # Salvar os dados dos trechos em cada arquivo
    with open(caminho_arquivo, 'wb') as f:
        pickle.dump(dados_trechos, f)
