import pickle

trechos = [
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

with open("trechos_server_c.plk", 'wb') as f:
    pickle.dump(trechos, f)
