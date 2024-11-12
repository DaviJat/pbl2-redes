import os
import pickle
import threading
import requests
import networkx as nx
import time

server_id = "C"
clock = 0
queue = []
lock = threading.Lock()

critical_section_lock = threading.Lock()

def lamport_clock():
    global clock
    with lock:
        clock += 1
    return clock

def process_purchase(trechos):
    servidor_urls = {"a": "http://localhost:5000", "b": "http://localhost:5001", "c": "http://localhost:5002"}

    for trecho in trechos["rota"]:
        server_url = servidor_urls.get(trecho["servidor"].lower())
        if server_url:
            try:
                # Verifique o status do trecho antes de comprar
                response = requests.get(f"{server_url}/check_trecho_status", json={"id": trecho["id"]})
                
                if response.status_code == 200 and response.json().get("disponivel", False):
                    # Se disponível, tente comprar o trecho
                    response = requests.post(f"{server_url}/update_trecho", json=trecho)
                    if response.status_code == 200:
                        print(f"Trecho comprado e atualizado: {trecho}")
                    else:
                        print(f"Falha ao atualizar trecho: {trecho}, motivo: {response.status_code}")
                        break  # Parar a operação se o trecho não puder ser comprado
                else:
                    print(f"Trecho não disponível para compra: {trecho}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão com {server_url}: {e}")
                break  # Se não conseguir conexão, parar a operação

def release_access(request, other_servers):
    global queue
    queue = [req for req in queue if req != request]

    for server in other_servers:
        try:
            response = requests.post(f"{server}/release", json={"server_id": request["server_id"], "id": request["id"]})
            print(f"Liberação enviada para {server}, status: {response.status_code}")

            # Atualize os trechos vendidos globalmente
            for trecho in request["trechos"]["rota"]:
                requests.post(f"{server}/update_global_status", json=trecho)
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com {server}: {e}")

def request_purchase(trechos, other_servers):
    global queue
    timestamp = lamport_clock()
    request = {"id": timestamp, "server_id": server_id, "trechos": trechos}
    queue.append(request)

    for server in other_servers:
        try:
            response = requests.post(f"{server}/purchase_request", json=request)
            print(f"Requisição de compra enviada para {server}, status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com {server}: {e}")

    while not is_top_of_queue(request):
        time.sleep(0.1)

    with critical_section_lock:
        print("Acessando seção crítica para processar compra.")
        process_purchase(trechos)

    release_access(request, other_servers)

def is_top_of_queue(request):
    sorted_queue = sorted(queue, key=lambda x: (x["id"], x["server_id"]))
    return sorted_queue[0] == request if sorted_queue else False

def load_trechos(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return []

def fetch_trechos_from_servers(servers):
    all_trechos = []
    for server_url in servers:
        try:
            response = requests.get(f"{server_url}/return_trechos")
            print(f"Dados recebidos de {server_url}: {response.status_code}")
            all_trechos.extend(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o servidor {server_url}: {e}")
    return all_trechos

def create_graph(trechos):
    grafo = nx.DiGraph()
    for trecho in trechos:
        if trecho["quantidade_passagens"] > 0:
            grafo.add_edge(
                trecho["origem"],
                trecho["destino"],
                id=trecho["id"],
                distancia=trecho["distancia"],
                passagens=trecho["quantidade_passagens"],
                servidor=trecho["servidor"]
            )
    return grafo


def create_routes(grafo, origem, destino):
    rotas = []
    rotas_unicas = set()
    try:
        all_paths = list(nx.all_simple_paths(grafo, source=origem, target=destino))

        for path in all_paths:
            trechos_rota = get_trechos_da_rota(grafo, path)
            rota_str = " -> ".join([f"{trecho['origem']}->{trecho['destino']}" for trecho in trechos_rota])
            if rota_str not in rotas_unicas:
                rotas_unicas.add(rota_str)
                rotas.append((trechos_rota, sum(trecho['distancia'] for trecho in trechos_rota)))

        rotas = [rota[0] for rota in sorted(rotas, key=lambda x: x[1])[:10]]
    except nx.NetworkXNoPath:
        print("Nenhum caminho encontrado.")
    return rotas

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
