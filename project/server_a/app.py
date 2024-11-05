import os
import pickle
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import create_routes, fetch_trechos_from_servers, load_trechos, create_graph, request_purchase

# Inicialização do aplicativo Flask e configuração de CORS
app = Flask(__name__)
CORS(app)

# Configurações do servidor
server_id = "A"  # Identificação do servidor atual
locks = {}  # Dicionário de locks para cada trecho
filename = os.path.join("project", "server_a", "trechos_server_a.plk")  # Caminho do arquivo de dados
other_servers = ["http://localhost:5001", "http://localhost:5002"]  # URLs dos outros servidores

# Variáveis globais para controle de Lamport
clock = 0  # Relógio lógico para controle de requisições
queue = []  # Fila de requisições para controle de concorrência

def acquire_lock(trecho_id):
    """Função para adquirir lock para um trecho específico."""
    if trecho_id not in locks:
        locks[trecho_id] = threading.Lock()  # Cria um lock para o trecho se não existir
    return locks[trecho_id]

@app.route('/trechos', methods=['GET'])
def get_trechos():
    origem = request.args.get('origem', '')
    destino = request.args.get('destino', '')
    all_servers = ["http://127.0.0.1:5000"] + other_servers

    print(f"Obtendo trechos dos servidores: {all_servers}")

    all_trechos = fetch_trechos_from_servers(all_servers)
    trechos_in_graph = create_graph(all_trechos)
    all_routes = create_routes(trechos_in_graph, origem, destino)

    return jsonify(all_routes), 200

@app.route('/return_trechos', methods=['GET'])
def return_trechos():
    trechos = load_trechos(filename)
    return jsonify(trechos), 200

@app.route('/comprar', methods=['POST'])
def comprar():
    data = request.get_json()
    print(f"Recebido pedido de compra: {data}")
    
    try:
        # Adquire locks de cada trecho antes de realizar a compra
        acquired_locks = []
        for trecho in data["rota"]:
            trecho_id = trecho["id"]
            trecho_lock = acquire_lock(trecho_id)
            trecho_lock.acquire()
            acquired_locks.append(trecho_lock)

        # Verifica se todos os trechos ainda têm passagens disponíveis
        trechos = load_trechos(filename)
        for trecho in data["rota"]:
            matching_trecho = next((t for t in trechos if t["id"] == trecho["id"] and t["servidor"] == trecho["servidor"]), None)
            if not matching_trecho or matching_trecho["quantidade_passagens"] < 1:
                raise ValueError("Trecho indisponível")

        # Processa a compra enquanto os trechos estão bloqueados
        request_purchase(data, other_servers)

        # Libera todos os locks após o processamento
        for lock in acquired_locks:
            lock.release()

        return jsonify({"status": "success", "message": "Compra realizada com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao processar compra: {e}")
        # Libera todos os locks em caso de erro
        for lock in acquired_locks:
            if lock.locked():
                lock.release()
        return jsonify({"status": "error", "message": "Erro ao realizar a compra"}), 500

@app.route('/purchase_request', methods=['POST'])
def receive_purchase_request():
    global clock, queue
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    clock = max(clock, data["id"]) + 1
    queue.append(data)
    print(f"Requisição de compra recebida de {data['server_id']} com timestamp {data['id']}")

    return jsonify({"message": "Compra request received", "clock": clock}), 200

@app.route('/release', methods=['POST'])
def receive_release():
    global queue
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    queue = [req for req in queue if not (req["id"] == data["id"] and req["server_id"] == data["server_id"])]
    print(f"Liberação recebida de {data['server_id']} para timestamp {data['id']}")

    return jsonify({"message": "Release received"}), 200

@app.route('/update_trecho', methods=['POST'])
def update_trecho():
    trecho_data = request.get_json()
    trecho_id = trecho_data["id"]
    trecho_servidor = trecho_data["servidor"]

    trechos = load_trechos(filename)

    for trecho in trechos:
        if trecho["id"] == trecho_id and trecho["servidor"] == trecho_servidor:
            if trecho["quantidade_passagens"] > 1:
                trecho["quantidade_passagens"] -= 1
                print(f"Atualizado trecho: {trecho}")
            else:
                trechos.remove(trecho)
                print(f"Removido trecho por falta de passagens: {trecho}")

            with open(filename, 'wb') as f:
                pickle.dump(trechos, f)

            return jsonify({"message": "Trecho atualizado com sucesso"}), 200

    return jsonify({"error": "Trecho não encontrado"}), 404

if __name__ == "__main__":
    app.run(port=5000)
