import pickle

trechos = [
    {"id": 1, "origem": "Rio de Janeiro", "destino": "Porto Alegre", "distancia": 1550, "quantidade_passagens": 2},
    {"id": 2, "origem": "Brasília", "destino": "Salvador", "distancia": 1440, "quantidade_passagens": 6},
    {"id": 3, "origem": "Brasília", "destino": "Fortaleza", "distancia": 2200, "quantidade_passagens": 2},
    {"id": 4, "origem": "Brasília", "destino": "Belo Horizonte", "distancia": 740, "quantidade_passagens": 7},
    {"id": 5, "origem": "Brasília", "destino": "Manaus", "distancia": 3490, "quantidade_passagens": 1},
    {"id": 6, "origem": "Brasília", "destino": "Curitiba", "distancia": 1370, "quantidade_passagens": 5},
    {"id": 7, "origem": "Brasília", "destino": "Recife", "distancia": 2200, "quantidade_passagens": 3},
    {"id": 8, "origem": "Brasília", "destino": "Porto Alegre", "distancia": 2020, "quantidade_passagens": 4},
    {"id": 9, "origem": "Salvador", "destino": "Fortaleza", "distancia": 1020, "quantidade_passagens": 3},
    {"id": 10, "origem": "Salvador", "destino": "Belo Horizonte", "distancia": 1370, "quantidade_passagens": 6},
    {"id": 11, "origem": "Salvador", "destino": "Manaus", "distancia": 4430, "quantidade_passagens": 2},
    {"id": 12, "origem": "Salvador", "destino": "Curitiba", "distancia": 2290, "quantidade_passagens": 4},
    {"id": 13, "origem": "Salvador", "destino": "Recife", "distancia": 800, "quantidade_passagens": 5},
    {"id": 14, "origem": "Salvador", "destino": "Porto Alegre", "distancia": 3070, "quantidade_passagens": 2},
    {"id": 15, "origem": "Fortaleza", "destino": "Belo Horizonte", "distancia": 2520, "quantidade_passagens": 3},
    {"id": 16, "origem": "Fortaleza", "destino": "Manaus", "distancia": 5680, "quantidade_passagens": 1}
]


with open("trechos_server_b.plk", 'wb') as f:
    pickle.dump(trechos, f)
