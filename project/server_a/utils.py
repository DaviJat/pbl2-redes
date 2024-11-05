import os
import pickle
import threading
import requests
import networkx as nx
import time

# Identificação do servidor
server_id = "A"

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

def process_purchase(trechos):
    # Dicionário que associa cada servidor com seu URL
    servidor_urls = {
        "a": "http://localhost:5000",
        "b": "http://localhost:5001",
        "c": "http://localhost:5002"
    }

    for trecho in trechos["rota"]:
        servidor = trecho["servidor"].lower()
        server_url = servidor_urls.get(servidor)

        if server_url:
            try:
                response = requests.post(f"{server_url}/update_trecho", json=trecho)
                if response.status_code == 200:
                    print(f"Atualização enviada para {server_url} para o trecho {trecho['id']}")
                else:
                    print(f"Erro ao enviar atualização para {server_url}: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão com {server_url}: {e}")
        else:
            print(f"URL para o servidor {servidor} não encontrada.")

# Envia uma solicitação de compra com exclusão mútua usando o Algoritmo de Lamport
def request_purchase(trechos, other_servers):
    global queue
    timestamp = lamport_clock()
    request = {"id": timestamp, "server_id": server_id, "trechos": trechos}
    queue.append(request)  # Adiciona a própria requisição à fila

    # Envia a requisição para os outros servidores
    for server in other_servers:
        try:
            response = requests.post(f"{server}/purchase_request", json=request)
            if response.status_code == 200:
                print(f"Requisição de compra enviada para {server} com sucesso.")
            else:
                print(f"Erro ao enviar requisição de compra para {server}")
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com {server}: {e}")

    # Aguarda respostas e verifica a fila
    while not is_top_of_queue(request):
        time.sleep(0.1)  # Espera até que a requisição esteja no topo da fila

    print("Entrando na seção crítica para realizar a compra")
    # Realiza a compra
    process_purchase(trechos)

    # Remove a requisição da fila após a seção crítica
    release_access(request, other_servers)

# Verifica se a requisição está no topo da fila para permitir acesso à seção crítica
def is_top_of_queue(request):
    # Ordena a fila de requisições
    sorted_queue = sorted(queue, key=lambda x: (x["id"], x["server_id"]))
    return sorted_queue[0] == request

# Libera o acesso após sair da seção crítica
def release_access(request, other_servers):
    # Remove a requisição da fila e notifica outros servidores
    global queue
    queue = [req for req in queue if req != request]

    # Envia a mensagem de liberação para os outros servidores
    for server in other_servers:
        try:
            response = requests.post(f"{server}/release", json={"server_id": request["server_id"], "id": request["id"]})
            if response.status_code == 200:
                print(f"Liberação enviada para {server}")
            else:
                print(f"Erro ao enviar liberação para {server}")
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com {server}: {e}")

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

# Função para criar um grafo direcionado dos trechos enviados
def create_graph(trechos):
    grafo = nx.DiGraph()  # Grafo direcionado
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

# Função para pegar os 10 menores caminhos entre origem e destino
def create_routes(grafo, origem, destino):
    rotas = []
    rotas_unicas = set()  # Conjunto para controlar rotas únicas

    try:
        # Obter todas as rotas possíveis entre origem e destino com até 10 rotas únicas
        all_paths = list(nx.all_simple_paths(grafo, source=origem, target=destino))
        
        # Avaliar cada rota, calcular a distância total e verificar unicidade
        for path in all_paths:
            trechos_rota = get_trechos_da_rota(grafo, path)
            rota_str = " -> ".join([f"{trecho['origem']}->{trecho['destino']}" for trecho in trechos_rota])
            
            # Adicionar rota se for única
            if rota_str not in rotas_unicas:
                rotas_unicas.add(rota_str)
                rotas.append((trechos_rota, sum(trecho['distancia'] for trecho in trechos_rota)))

        # Ordenar as rotas pela distância total e limitar às 10 melhores
        rotas = sorted(rotas, key=lambda x: x[1])[:10]
        
        # Extrair apenas os trechos de cada rota para a resposta final
        rotas = [rota[0] for rota in rotas]

    except nx.NetworkXNoPath:
        return []  # Retorna vazio se não houver caminho

    return rotas

# Função auxiliar para obter trechos completos da rota
def get_trechos_da_rota(grafo, rota):
    return [
        {
            "id": grafo[rota[i]][rota[i + 1]]["id"],
            "servidor": grafo[rota[i]][rota[i + 1]]["servidor"],
            "origem": rota[i],
            "destino": rota[i + 1],
            "distancia": grafo[rota[i]][rota[i + 1]]["distancia"],
            "quantidade_passagens": grafo[rota[i]][rota[i + 1]]["passagens"]
        }
        for i in range(len(rota) - 1)
    ]
