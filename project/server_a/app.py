import os
import pickle
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from utils import create_routes, fetch_trechos_from_servers, load_trechos, create_graph

# Inicialização do aplicativo Flask e configuração de CORS
app = Flask(__name__)
CORS(app)

# Configurações do servidor
server_id = "a"  # Mude este valor para "a", "b", ou "c" conforme o servidor
other_servers = {
    "a": "http://127.0.0.1:5000",
    "b": "http://127.0.0.1:5001",
    "c": "http://127.0.0.1:5002"
}

# Caminho do arquivo de dados
filename = os.path.join("project", f"server_{server_id}", f"trechos_server_{server_id}.plk")

# Variáveis globais para controle de Lamport, concorrência e locks
clock = 0
queue = []
locks = {}  # Dicionário de locks para cada trecho

def acquire_lock(trecho_id):
    """Função para adquirir lock para um trecho específico."""
    if trecho_id not in locks:
        locks[trecho_id] = threading.Lock()  # Cria um lock para o trecho se não existir
    return locks[trecho_id]

@app.route('/trechos', methods=['GET'])
def get_trechos():
    origem = request.args.get('origem', '')
    destino = request.args.get('destino', '')
    all_servers = [f"http://127.0.0.1:500{port}" for port in range(3)]

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
        for trecho in data["rota"]:
            trecho_id = trecho["id"]
            trecho_servidor = trecho["servidor"]

            # Verifique se o trecho pertence ao servidor atual ou a outro
            if trecho_servidor != server_id:
                # Redirecione a requisição para o servidor proprietário do trecho
                server_url = other_servers.get(trecho_servidor)
                if server_url:
                    print(f"Redirecionando a compra para o servidor {trecho_servidor.upper()}")
                    response = requests.post(f"{server_url}/comprar", json=data)
                    return response.content, response.status_code
                else:
                    return jsonify({"error": "Servidor proprietário não encontrado"}), 400

        # Adquire locks para cada trecho local (pertencente a este servidor)
        acquired_locks = []
        trechos = load_trechos(filename)
        
        for trecho in data["rota"]:
            matching_trecho = next((t for t in trechos if t["id"] == trecho["id"] and t["servidor"] == trecho["servidor"]), None)
            if not matching_trecho or matching_trecho["quantidade_passagens"] < 1:
                raise ValueError("Trecho indisponível")
            
            trecho_lock = acquire_lock(trecho["id"])
            trecho_lock.acquire()
            acquired_locks.append(trecho_lock)

        # Processa a compra enquanto os trechos estão bloqueados
        for trecho in data["rota"]:
            for t in trechos:
                if t["id"] == trecho["id"] and t["servidor"] == trecho["servidor"]:
                    t["quantidade_passagens"] -= 1
                    print(f"Trecho atualizado: {t}")

        # Salva as alterações
        with open(filename, 'wb') as f:
            pickle.dump(trechos, f)

        # Libera os locks após o processamento
        for lock in acquired_locks:
            lock.release()

        return jsonify({"status": "success", "message": "Compra realizada com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao processar compra: {e}")
        for lock in acquired_locks:
            if lock.locked():
                lock.release()
        return jsonify({"status": "error", "message": "Erro ao realizar a compra"}), 500

@app.route('/check_trecho_status', methods=['GET'])
def check_trecho_status():
    data = request.get_json()
    trecho_id = data.get("id")
    trechos = load_trechos(filename)

    for trecho in trechos:
        if trecho["id"] == trecho_id and trecho["quantidade_passagens"] > 0:
            return jsonify({"disponivel": True}), 200
    return jsonify({"disponivel": False}), 404

if __name__ == "__main__":
    app.run(port=5000 if server_id == "a" else 5001 if server_id == "b" else 5002)
