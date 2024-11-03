import threading
import requests
import os
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
    with open(filename, 'r') as f:
        trechos = [line.strip() for line in f.readlines()]
    return trechos

# Função para remover um trecho do arquivo após compra
def remove_trecho(filename, trecho_id):
    if not os.path.exists(filename):
        return
    with open(filename, 'r') as f:
        trechos = f.readlines()
    with open(filename, 'w') as f:
        for trecho in trechos:
            if not trecho.startswith(f"{trecho_id},"):
                f.write(trecho)

# Enviar solicitação de reserva para outros servidores
def request_reservation(trecho, server_id, other_servers):
    timestamp = lamport_clock()
    queue.append((timestamp, server_id, trecho))

    # Enviar solicitação para os outros servidores
    for server_url in other_servers:
        try:
            requests.post(f"{server_url}/receive_request", json={"timestamp": timestamp, "server_id": server_id, "trecho": trecho})
        except Exception as e:
            print(f"Erro na comunicação com {server_url}: {e}")

# Receber requisição de outros servidores
def receive_request(data):
    timestamp = data["timestamp"]
    server_id = data["server_id"]
    trecho = data["trecho"]

    with lock:
        queue.append((timestamp, server_id, trecho))
        queue.sort()  # Ordena a fila para garantir a ordem de Lamport

# Confirmação de reserva do trecho
def confirm_reservation(trecho_id, server_id, filename):
    global queue
    with lock:
        # Remove requisições da fila
        queue = [req for req in queue if not (req[1] == server_id and req[2] == trecho_id)]
        
    # Remover o trecho do arquivo
    remove_trecho(filename, trecho_id)
    print(f"Servidor {server_id} confirmou a compra do trecho {trecho_id} e o removeu de {filename}.")

# Função para obter trechos de todos os servidores
def fetch_trechos_from_servers(servers):
    all_trechos = []
    for server_url in servers:
        try:
            print(f"{server_url}/return_trechos")
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
            rotas.append({"caminho": nova_rota, "distancia": nova_distancia})
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