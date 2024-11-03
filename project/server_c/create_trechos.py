import pickle

trechos = [
    {"id": 1, "rota": "Curitiba -> Florianópolis"},
    {"id": 2, "rota": "Florianópolis -> Porto Alegre"},
    {"id": 3, "rota": "Porto Alegre -> Caxias do Sul"},
    {"id": 4, "rota": "Caxias do Sul -> Londrina"},
    {"id": 5, "rota": "Londrina -> Maringá"},
    {"id": 6, "rota": "Maringá -> Foz do Iguaçu"},
    {"id": 7, "rota": "Foz do Iguaçu -> Cascavel"},
    {"id": 8, "rota": "Cascavel -> Campo Grande"},
    {"id": 9, "rota": "Campo Grande -> Cuiabá"},
    {"id": 10, "rota": "Cuiabá -> Goiânia"}
]

with open("trechos_server_c.plk", 'wb') as f:
    pickle.dump(trechos, f)
