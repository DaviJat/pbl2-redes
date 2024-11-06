import pickle
import os

trechos_a = [
    {"id": 1, "servidor": "a", "origem": "São Paulo", "destino": "Rio de Janeiro", "distancia": 430, "quantidade_passagens": 10},
    {"id": 2, "servidor": "a", "origem": "São Paulo", "destino": "Brasília", "distancia": 1015, "quantidade_passagens": 5},
    {"id": 3, "servidor": "a", "origem": "São Paulo", "destino": "Salvador", "distancia": 1960, "quantidade_passagens": 3},
    {"id": 4, "servidor": "a", "origem": "São Paulo", "destino": "Fortaleza", "distancia": 3120, "quantidade_passagens": 2},
    {"id": 5, "servidor": "a", "origem": "São Paulo", "destino": "Belo Horizonte", "distancia": 585, "quantidade_passagens": 8},
    {"id": 6, "servidor": "a", "origem": "São Paulo", "destino": "Manaus", "distancia": 3930, "quantidade_passagens": 4},
    {"id": 7, "servidor": "a", "origem": "São Paulo", "destino": "Curitiba", "distancia": 410, "quantidade_passagens": 6},
    {"id": 8, "servidor": "a", "origem": "São Paulo", "destino": "Recife", "distancia": 2670, "quantidade_passagens": 2},
    {"id": 9, "servidor": "a", "origem": "São Paulo", "destino": "Porto Alegre", "distancia": 1115, "quantidade_passagens": 5},
    {"id": 10, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Brasília", "distancia": 1160, "quantidade_passagens": 6},
    {"id": 11, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Salvador", "distancia": 1660, "quantidade_passagens": 4},
    {"id": 12, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Fortaleza", "distancia": 2800, "quantidade_passagens": 1},
    {"id": 13, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Belo Horizonte", "distancia": 440, "quantidade_passagens": 7},
    {"id": 14, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Manaus", "distancia": 3680, "quantidade_passagens": 3},
    {"id": 15, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Curitiba", "distancia": 850, "quantidade_passagens": 5},
    {"id": 16, "servidor": "a", "origem": "Rio de Janeiro", "destino": "Recife", "distancia": 2330, "quantidade_passagens": 3}
]

trechos_b = [
    {"id": 1, "servidor": "b", "origem": "Rio de Janeiro", "destino": "Porto Alegre", "distancia": 1550, "quantidade_passagens": 2},
    {"id": 2, "servidor": "b", "origem": "Brasília", "destino": "Salvador", "distancia": 1440, "quantidade_passagens": 6},
    {"id": 3, "servidor": "b", "origem": "Brasília", "destino": "Fortaleza", "distancia": 2200, "quantidade_passagens": 2},
    {"id": 4, "servidor": "b", "origem": "Brasília", "destino": "Belo Horizonte", "distancia": 740, "quantidade_passagens": 7},
    {"id": 5, "servidor": "b", "origem": "Brasília", "destino": "Manaus", "distancia": 3490, "quantidade_passagens": 1},
    {"id": 6, "servidor": "b", "origem": "Brasília", "destino": "Curitiba", "distancia": 1370, "quantidade_passagens": 5},
    {"id": 7, "servidor": "b", "origem": "Brasília", "destino": "Recife", "distancia": 2200, "quantidade_passagens": 3},
    {"id": 8, "servidor": "b", "origem": "Brasília", "destino": "Porto Alegre", "distancia": 2020, "quantidade_passagens": 4},
    {"id": 9, "servidor": "b", "origem": "Salvador", "destino": "Fortaleza", "distancia": 1020, "quantidade_passagens": 3},
    {"id": 10, "servidor": "b", "origem": "Salvador", "destino": "Belo Horizonte", "distancia": 1370, "quantidade_passagens": 6},
    {"id": 11, "servidor": "b", "origem": "Salvador", "destino": "Manaus", "distancia": 4430, "quantidade_passagens": 2},
    {"id": 12, "servidor": "b", "origem": "Salvador", "destino": "Curitiba", "distancia": 2290, "quantidade_passagens": 4},
    {"id": 13, "servidor": "b", "origem": "Salvador", "destino": "Recife", "distancia": 800, "quantidade_passagens": 5},
    {"id": 14, "servidor": "b", "origem": "Salvador", "destino": "Porto Alegre", "distancia": 3070, "quantidade_passagens": 2},
    {"id": 15, "servidor": "b", "origem": "Fortaleza", "destino": "Belo Horizonte", "distancia": 2520, "quantidade_passagens": 3},
    {"id": 16, "servidor": "b", "origem": "Fortaleza", "destino": "Manaus", "distancia": 5680, "quantidade_passagens": 1}
]

trechos_c = [
    {"id": 1, "servidor": "c", "origem": "Fortaleza", "destino": "Curitiba", "distancia": 3680, "quantidade_passagens": 2},
    {"id": 2, "servidor": "c", "origem": "Fortaleza", "destino": "Recife", "distancia": 800, "quantidade_passagens": 6},
    {"id": 3, "servidor": "c", "origem": "Fortaleza", "destino": "Porto Alegre", "distancia": 4570, "quantidade_passagens": 1},
    {"id": 4, "servidor": "c", "origem": "Belo Horizonte", "destino": "Manaus", "distancia": 3930, "quantidade_passagens": 2},
    {"id": 5, "servidor": "c", "origem": "Belo Horizonte", "destino": "Curitiba", "distancia": 1000, "quantidade_passagens": 4},
    {"id": 6, "servidor": "c", "origem": "Belo Horizonte", "destino": "Recife", "distancia": 2090, "quantidade_passagens": 3},
    {"id": 7, "servidor": "c", "origem": "Belo Horizonte", "destino": "Porto Alegre", "distancia": 1710, "quantidade_passagens": 5},
    {"id": 8, "servidor": "c", "origem": "Manaus", "destino": "Curitiba", "distancia": 4360, "quantidade_passagens": 1},
    {"id": 9, "servidor": "c", "origem": "Manaus", "destino": "Recife", "distancia": 5900, "quantidade_passagens": 1},
    {"id": 10, "servidor": "c", "origem": "Manaus", "destino": "Porto Alegre", "distancia": 4900, "quantidade_passagens": 1},
    {"id": 11, "servidor": "c", "origem": "Curitiba", "destino": "Recife", "distancia": 3030, "quantidade_passagens": 2},
    {"id": 12, "servidor": "c", "origem": "Curitiba", "destino": "Porto Alegre", "distancia": 710, "quantidade_passagens": 7},
    {"id": 13, "servidor": "c", "origem": "Recife", "destino": "Porto Alegre", "distancia": 3700, "quantidade_passagens": 2}
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
