import os
import pickle
import threading
import requests
import networkx as nx

# Variáveis de exclusão mútua
clock = 0
queue = []
lock = threading.Lock()

# Função do relógio lógico de Lamport
def lamport_clock():
    global clock
    with lock:
        clock += 1
    return clock

# Função para carregar trechos de um arquivo específico
def load_trechos(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Função para obter trechos de todos os servidores
def fetch_trechos_from_servers(servers):
    all_trechos = []
    for server_url in servers:
        try:
            response = requests.get(f"{server_url}/return_trechos")
            if response.status_code == 200:
                all_trechos.extend(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o servidor {server_url}: {e}")
    return all_trechos

# Função para pegar os 10 menores caminhos entre origem e destino
def create_routes(grafo, origem, destino):
    rotas = []
    try:
        # Encontrar a rota inicial e coletar dados dos trechos completos
        rota_inicial = nx.shortest_path(grafo, source=origem, target=destino, weight='distancia')
        trechos_rota_inicial = [
            {
                "id": grafo[rota_inicial[i]][rota_inicial[i + 1]]["id"],
                "servidor": grafo[rota_inicial[i]][rota_inicial[i + 1]]["servidor"],
                "origem": rota_inicial[i],
                "destino": rota_inicial[i + 1],
                "distancia": grafo[rota_inicial[i]][rota_inicial[i + 1]]["distancia"],
                "quantidade_passagens": grafo[rota_inicial[i]][rota_inicial[i + 1]]["passagens"]
            }
            for i in range(len(rota_inicial) - 1)
        ]
        rotas.append(trechos_rota_inicial)
    except nx.NetworkXNoPath:
        return []  # Retorna vazio se não houver caminho

    # Encontrar até 10 caminhos alternativos
    for _ in range(10):
        try:
            # Remover a rota atual para forçar uma nova rota
            grafo.remove_edges_from(
                [(rota_inicial[i], rota_inicial[i + 1]) for i in range(len(rota_inicial) - 1)]
            )
            nova_rota = nx.shortest_path(grafo, source=origem, target=destino, weight='distancia')
            trechos_nova_rota = [
                {
                    "id": grafo[nova_rota[i]][nova_rota[i + 1]]["id"],
                    "servidor": grafo[nova_rota[i]][nova_rota[i + 1]]["servidor"],
                    "origem": nova_rota[i],
                    "destino": nova_rota[i + 1],
                    "distancia": grafo[nova_rota[i]][nova_rota[i + 1]]["distancia"],
                    "quantidade_passagens": grafo[nova_rota[i]][nova_rota[i + 1]]["passagens"]
                }
                for i in range(len(nova_rota) - 1)
            ]
            rotas.append(trechos_nova_rota)
            rota_inicial = nova_rota  # Atualizar para a próxima iteração
        except nx.NetworkXNoPath:
            break  # Termina se não encontrar um novo caminho

    return rotas

# Função para criar um grafo totalmente relacionado dos trechos enviados
def create_graph(trechos):
    grafo = nx.Graph()
    for trecho in trechos:
        origem = trecho["origem"]
        destino = trecho["destino"]
        distancia = trecho["distancia"]
        passagens = trecho["quantidade_passagens"]
        trecho_id = trecho["id"]
        servidor = trecho["servidor"]

        grafo.add_edge(
            origem,
            destino,
            id=trecho_id,
            distancia=distancia,
            passagens=passagens,
            servidor=servidor  # Adiciona o servidor ao grafo
        )
    return grafo
