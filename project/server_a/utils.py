import threading
import requests
import os

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
