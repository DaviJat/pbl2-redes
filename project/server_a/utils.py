# utils.py

import os
import pickle
import threading
import requests
import networkx as nx
import time

# Configuração de exclusão mútua para Lamport Clock
server_id = "A"  # Identificação do servidor
clock = 0  # Relógio lógico para controle de concorrência
queue = []  # Fila de requisições para controle de seção crítica
lock = threading.Lock()  # Lock para manipulação de exclusão mútua

def lamport_clock():
    # Função para incrementar o relógio lógico com exclusão mútua
    global clock
    with lock:
        clock += 1  # Incrementa o clock protegido pelo lock
    return clock

def process_purchase(trechos):
    # Função para processar compra de trechos em servidores específicos
    servidor_urls = {"a": "http://localhost:5000", "b": "http://localhost:5001", "c": "http://localhost:5002"}  # URLs dos servidores

    # Envia atualização para cada trecho da rota
    for trecho in trechos["rota"]:
        server_url = servidor_urls.get(trecho["servidor"].lower())  # URL do servidor do trecho
        if server_url:
            try:
                response = requests.post(f"{server_url}/update_trecho", json=trecho)
                print(f"Processamento de compra no servidor {server_url} para trecho {trecho['id']}, status: {response.status_code}")  # Log do status
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão com {server_url}: {e}")  # Log de erro de conexão

def request_purchase(trechos, other_servers):
    # Função para realizar solicitação de compra com controle de Lamport
    global queue
    timestamp = lamport_clock()  # Gera timestamp único
    request = {"id": timestamp, "server_id": server_id, "trechos": trechos}
    queue.append(request)  # Adiciona a requisição na fila

    # Envia a requisição de compra para outros servidores
    for server in other_servers:
        try:
            response = requests.post(f"{server}/purchase_request", json=request)
            print(f"Requisição de compra enviada para {server}, status: {response.status_code}")  # Log do envio
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com {server}: {e}")  # Log de erro de conexão

    # Espera até que a requisição esteja no topo da fila para acessar a seção crítica
    while not is_top_of_queue(request):
        time.sleep(0.1)  # Intervalo de espera para evitar busy-waiting

    print("Acessando seção crítica para processar compra.")  # Log de acesso à seção crítica
    process_purchase(trechos)
    release_access(request, other_servers)  # Libera o acesso após concluir

def is_top_of_queue(request):
    # Verifica se a requisição está no topo da fila
    sorted_queue = sorted(queue, key=lambda x: (x["id"], x["server_id"]))
    return sorted_queue[0] == request  # Retorna verdadeiro se a requisição é a primeira da fila

def release_access(request, other_servers):
    # Função para liberar a seção crítica após processamento
    global queue
    queue = [req for req in queue if req != request]  # Remove a requisição da fila

    # Envia a mensagem de liberação para outros servidores
    for server in other_servers:
        try:
            response = requests.post(f"{server}/release", json={"server_id": request["server_id"], "id": request["id"]})
            print(f"Liberação enviada para {server}, status: {response.status_code}")  # Log da liberação
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão com {server}: {e}")  # Log de erro de conexão

def load_trechos(filename):
    # Função para carregar trechos de um arquivo
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return []

def fetch_trechos_from_servers(servers):
    # Função para obter trechos de todos os servidores
    all_trechos = []
    for server_url in servers:
        try:
            response = requests.get(f"{server_url}/return_trechos")
            print(f"Dados recebidos de {server_url}: {response.status_code}")  # Log do status de resposta
            all_trechos.extend(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o servidor {server_url}: {e}")  # Log de erro de acesso
    return all_trechos

def create_graph(trechos):
    # Função para criar um grafo direcionado com os trechos
    grafo = nx.DiGraph()  # Cria um grafo direcionado
    for trecho in trechos:
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
    # Função para criar até 10 rotas únicas entre origem e destino
    rotas = []
    rotas_unicas = set()  # Conjunto para controle de rotas únicas
    try:
        all_paths = list(nx.all_simple_paths(grafo, source=origem, target=destino))  # Todas as rotas possíveis

        for path in all_paths:
            trechos_rota = get_trechos_da_rota(grafo, path)  # Detalhes dos trechos da rota
            rota_str = " -> ".join([f"{trecho['origem']}->{trecho['destino']}" for trecho in trechos_rota])
            if rota_str not in rotas_unicas:
                rotas_unicas.add(rota_str)
                rotas.append((trechos_rota, sum(trecho['distancia'] for trecho in trechos_rota)))

        rotas = [rota[0] for rota in sorted(rotas, key=lambda x: x[1])[:10]]  # Seleciona as 10 melhores rotas
    except nx.NetworkXNoPath:
        print("Nenhum caminho encontrado.")  # Log caso não haja caminho entre origem e destino
    return rotas

def get_trechos_da_rota(grafo, rota):
    # Função auxiliar para obter trechos completos de uma rota
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
