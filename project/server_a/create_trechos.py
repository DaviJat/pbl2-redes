import pickle

trechos = [
    {"id": 1, "rota": "Belém -> Fortaleza"},
    {"id": 2, "rota": "Fortaleza -> Manaus"},
    {"id": 3, "rota": "Manaus -> São Paulo"},
    {"id": 4, "rota": "São Paulo -> Salvador"},
    {"id": 5, "rota": "Salvador -> Recife"},
    {"id": 6, "rota": "Recife -> Brasília"},
    {"id": 7, "rota": "Brasília -> Curitiba"},
    {"id": 8, "rota": "Curitiba -> Porto Alegre"},
    {"id": 9, "rota": "Porto Alegre -> Rio de Janeiro"},
    {"id": 10, "rota": "Rio de Janeiro -> Belo Horizonte"}
]

with open("trechos_server_a.plk", 'wb') as f:
    pickle.dump(trechos, f)