# Função para pegar os 10 menores caminhos entre origem e destino
import networkx as nx


def create_routes(grafo, origem, destino):
    rotas = []

    try:
        rota_inicial = nx.shortest_path(grafo, source=origem, target=destino, weight='distancia')
        distancia_rota = nx.shortest_path_length(grafo, source=origem, target=destino, weight='distancia')
        rotas.append({"rota": rota_inicial, "distancia": distancia_rota})
    except nx.NetworkXNoPath:
        return [] # Retorna vazio se não houver caminho

    # Encontrar até 10 caminhos alternativos
    for i in range(1, 10):
        try:
            # Remover a rota atual para forçar uma nova rota
            grafo.remove_edges_from(
                [(rota_inicial[i], rota_inicial[i + 1]) for i in range(len(rota_inicial) - 1)])
            nova_rota = nx.shortest_path(grafo, source=origem, target=destino, weight='distancia')
            nova_distancia = nx.shortest_path_length(grafo, source=origem, target=destino, weight='distancia')
            rotas.append({"rota": nova_rota, "distancia": nova_distancia})
            rota_inicial = nova_rota
        except nx.NetworkXNoPath:
            break  # Se não encontrar caminho, termina

    return rotas

# função para criar um grafo totalmente relacionado dos trechos enviados
def create_graph(trechos):
    grafo = nx.Graph()

    for trecho in trechos:
        origem = trecho["origem"]
        destino = trecho["destino"]
        distancia = trecho["distancia"]
        passagens = trecho["quantidade_passagens"]
        trecho_id = trecho["id"]

        grafo.add_edge(
            origem,
            destino,
            id=trecho_id,
            distancia=distancia,
            passagens=passagens
        )

    return grafo

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

a = create_routes(create_graph(trechos), "São Paulo", "Rio de Janeiro")
for i in a:
    print(i)

