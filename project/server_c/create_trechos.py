import pickle

trechos = [
    {"id": 1, "origem": "Curitiba", "destino": "São Paulo", "distancia": 410, "quantidade_passagens": 7},
    {"id": 2, "origem": "Curitiba", "destino": "Rio de Janeiro", "distancia": 850, "quantidade_passagens": 4},
    {"id": 3, "origem": "Curitiba", "destino": "Salvador", "distancia": 2350, "quantidade_passagens": 3},
    {"id": 4, "origem": "Curitiba", "destino": "Belo Horizonte", "distancia": 1000, "quantidade_passagens": 5},
    {"id": 5, "origem": "Curitiba", "destino": "Manaus", "distancia": 3600, "quantidade_passagens": 2},
    {"id": 6, "origem": "Porto Alegre", "destino": "Brasília", "distancia": 1900, "quantidade_passagens": 3},
    {"id": 7, "origem": "Porto Alegre", "destino": "Recife", "distancia": 3200, "quantidade_passagens": 2},
    {"id": 8, "origem": "Porto Alegre", "destino": "Fortaleza", "distancia": 3800, "quantidade_passagens": 1},
    {"id": 9, "origem": "Porto Alegre", "destino": "São Paulo", "distancia": 1115, "quantidade_passagens": 6},
    {"id": 10, "origem": "Porto Alegre", "destino": "Curitiba", "distancia": 710, "quantidade_passagens": 4},
]
with open("trechos_server_c.plk", 'wb') as f:
    pickle.dump(trechos, f)
