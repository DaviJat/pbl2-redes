import pickle

trechos = [
    {"id": 1, "origem": "São Paulo", "destino": "Rio de Janeiro", "distancia": 430, "quantidade_passagens": 10},
    {"id": 2, "origem": "São Paulo", "destino": "Brasília", "distancia": 1015, "quantidade_passagens": 5},
    {"id": 3, "origem": "São Paulo", "destino": "Salvador", "distancia": 1960, "quantidade_passagens": 3},
    {"id": 4, "origem": "São Paulo", "destino": "Fortaleza", "distancia": 3120, "quantidade_passagens": 2},
    {"id": 5, "origem": "São Paulo", "destino": "Belo Horizonte", "distancia": 585, "quantidade_passagens": 8},
    {"id": 6, "origem": "São Paulo", "destino": "Manaus", "distancia": 3930, "quantidade_passagens": 4},
    {"id": 7, "origem": "São Paulo", "destino": "Curitiba", "distancia": 410, "quantidade_passagens": 6},
    {"id": 8, "origem": "São Paulo", "destino": "Recife", "distancia": 2670, "quantidade_passagens": 2},
    {"id": 9, "origem": "São Paulo", "destino": "Porto Alegre", "distancia": 1115, "quantidade_passagens": 5},
    {"id": 10, "origem": "Rio de Janeiro", "destino": "Brasília", "distancia": 1160, "quantidade_passagens": 6},
    {"id": 11, "origem": "Rio de Janeiro", "destino": "Salvador", "distancia": 1660, "quantidade_passagens": 4},
    {"id": 12, "origem": "Rio de Janeiro", "destino": "Fortaleza", "distancia": 2800, "quantidade_passagens": 1},
    {"id": 13, "origem": "Rio de Janeiro", "destino": "Belo Horizonte", "distancia": 440, "quantidade_passagens": 7},
    {"id": 14, "origem": "Rio de Janeiro", "destino": "Manaus", "distancia": 3680, "quantidade_passagens": 3},
    {"id": 15, "origem": "Rio de Janeiro", "destino": "Curitiba", "distancia": 850, "quantidade_passagens": 5},
    {"id": 16, "origem": "Rio de Janeiro", "destino": "Recife", "distancia": 2330, "quantidade_passagens": 3}
]

with open("trechos_server_a.plk", 'wb') as f:
    pickle.dump(trechos, f)
