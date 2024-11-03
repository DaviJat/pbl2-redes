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

with open("trechos_server_a.plk", 'wb') as f:
    pickle.dump(trechos, f)

with open("trechos_server_b.plk", 'wb') as f:
    pickle.dump(trechos, f)

with open("trechos_server_c.plk", 'wb') as f:
    pickle.dump(trechos, f)
