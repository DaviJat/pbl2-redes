import pickle

trechos_a = [
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

trechos_b = [
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

trechos_c = [
    {"id": 1, "origem": "Fortaleza", "destino": "Curitiba", "distancia": 3680, "quantidade_passagens": 2},
    {"id": 2, "origem": "Fortaleza", "destino": "Recife", "distancia": 800, "quantidade_passagens": 6},
    {"id": 3, "origem": "Fortaleza", "destino": "Porto Alegre", "distancia": 4570, "quantidade_passagens": 1},
    {"id": 4, "origem": "Belo Horizonte", "destino": "Manaus", "distancia": 3930, "quantidade_passagens": 2},
    {"id": 5, "origem": "Belo Horizonte", "destino": "Curitiba", "distancia": 1000, "quantidade_passagens": 4},
    {"id": 6, "origem": "Belo Horizonte", "destino": "Recife", "distancia": 2090, "quantidade_passagens": 3},
    {"id": 7, "origem": "Belo Horizonte", "destino": "Porto Alegre", "distancia": 1710, "quantidade_passagens": 5},
    {"id": 8, "origem": "Manaus", "destino": "Curitiba", "distancia": 4360, "quantidade_passagens": 1},
    {"id": 9, "origem": "Manaus", "destino": "Recife", "distancia": 5900, "quantidade_passagens": 1},
    {"id": 10, "origem": "Manaus", "destino": "Porto Alegre", "distancia": 4900, "quantidade_passagens": 1},
    {"id": 11, "origem": "Curitiba", "destino": "Recife", "distancia": 3030, "quantidade_passagens": 2},
    {"id": 12, "origem": "Curitiba", "destino": "Porto Alegre", "distancia": 710, "quantidade_passagens": 7},
    {"id": 13, "origem": "Recife", "destino": "Porto Alegre", "distancia": 3700, "quantidade_passagens": 2}
]

with open("trechos_server_a.plk", 'wb') as f:
    pickle.dump(trechos_a, f)

with open("trechos_server_b.plk", 'wb') as f:
    pickle.dump(trechos_b, f)

with open("trechos_server_c.plk", 'wb') as f:
    pickle.dump(trechos_c, f)
