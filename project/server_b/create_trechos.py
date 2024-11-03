import pickle

trechos = [
    {"id": 1, "origem": "Salvador", "destino": "São Paulo", "distancia": 1960, "quantidade_passagens": 4},
    {"id": 2, "origem": "Salvador", "destino": "Rio de Janeiro", "distancia": 1660, "quantidade_passagens": 3},
    {"id": 3, "origem": "Salvador", "destino": "Manaus", "distancia": 3120, "quantidade_passagens": 1},
    {"id": 4, "origem": "Salvador", "destino": "Curitiba", "distancia": 2350, "quantidade_passagens": 6},
    {"id": 5, "origem": "Salvador", "destino": "Recife", "distancia": 800, "quantidade_passagens": 4},
    {"id": 6, "origem": "Recife", "destino": "Fortaleza", "distancia": 800, "quantidade_passagens": 5},
    {"id": 7, "origem": "Recife", "destino": "Brasília", "distancia": 1650, "quantidade_passagens": 2},
    {"id": 8, "origem": "Recife", "destino": "São Paulo", "distancia": 2670, "quantidade_passagens": 3},
    {"id": 9, "origem": "Recife", "destino": "Porto Alegre", "distancia": 3400, "quantidade_passagens": 2},
    {"id": 10, "origem": "Recife", "destino": "Manaus", "distancia": 2850, "quantidade_passagens": 1},
]

with open("trechos_server_b.plk", 'wb') as f:
    pickle.dump(trechos, f)
