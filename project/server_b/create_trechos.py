import pickle

trechos = [
    {"id": 1, "rota": "Recife -> Fortaleza"},
    {"id": 2, "rota": "Fortaleza -> São Luís"},
    {"id": 3, "rota": "São Luís -> Belém"},
    {"id": 4, "rota": "Belém -> Teresina"},
    {"id": 5, "rota": "Teresina -> João Pessoa"},
    {"id": 6, "rota": "João Pessoa -> Natal"},
    {"id": 7, "rota": "Natal -> Maceió"},
    {"id": 8, "rota": "Maceió -> Aracaju"},
    {"id": 9, "rota": "Aracaju -> Salvador"},
    {"id": 10, "rota": "Salvador -> Vitória"}
]

with open("trechos_server_b.plk", 'wb') as f:
    pickle.dump(trechos, f)