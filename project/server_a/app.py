import os
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import create_routes, fetch_trechos_from_servers, load_trechos, create_graph, request_purchase

app = Flask(__name__)
CORS(app)

# Configurações específicas do servidor A
server_id = "A"
filename = os.path.join("project", "server_a", "trechos_server_a.plk")
other_servers = ["http://localhost:5001", "http://localhost:5002"]

# Variáveis globais para controle de Lamport
clock = 0
queue = []

def load_trechos(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return []

@app.route('/trechos', methods=['GET'])
def get_trechos():
    origem = request.args.get('origem', '')
    destino = request.args.get('destino', '')
    all_servers = ["http://127.0.0.1:5000"] + other_servers
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
    trechos = request.get_json()
    print(f"Recebido pedido de compra: {trechos}")
    request_purchase(trechos, other_servers)
    return 'Compra realizada com sucesso', 200

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

    # Carrega o arquivo de trechos
    trechos = load_trechos(filename)

    # Log inicial: Mostrar os trechos carregados antes da atualização
    print(f"[ANTES] Trechos em {filename}: {trechos}")

    # Busca o trecho pelo ID e servidor e realiza a atualização
    for trecho in trechos:
        if trecho["id"] == trecho_id and trecho["servidor"] == trecho_servidor:
            if trecho["quantidade_passagens"] > 1:
                trecho["quantidade_passagens"] -= 1
                print(f"Trem de {trecho['origem']} para {trecho['destino']} atualizado, nova quantidade: {trecho['quantidade_passagens']}")
            else:
                trechos.remove(trecho)
                print(f"Trem de {trecho['origem']} para {trecho['destino']} removido por falta de passagens")

            # Salva o arquivo atualizado
            with open(filename, 'wb') as f:
                pickle.dump(trechos, f)

            # Log final: Mostrar os trechos após a atualização
            print(f"[DEPOIS] Trechos em {filename}: {trechos}")

            return jsonify({"message": "Trecho atualizado com sucesso"}), 200

    # Retorna erro se o trecho não for encontrado
    return jsonify({"error": "Trecho não encontrado"}), 404

if __name__ == "__main__":
    app.run(port=5000)
