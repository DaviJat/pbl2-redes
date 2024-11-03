import os
import pickle
import threading
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import create_routes, fetch_trechos_from_servers, receive_request, confirm_purchase, load_trechos, create_graph, lamport_clock, queue, request_region_access

app = Flask(__name__)
CORS(app)

# Identificação do servidor e arquivo pickle de trechos
server_id = "B"
filename = os.path.join("project", "server_b", "trechos_server_b.plk")
other_servers = ["http://localhost:5000", "http://localhost:5002"]

# Carregar os trechos deste servidor
def load_trechos(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

@app.route('/trechos', methods=['GET'])
def get_trechos():
    origem = request.args.get('origem', '')
    destino = request.args.get('destino', '')
    all_servers = [f"http://127.0.0.1:5001"] + other_servers
    all_trechos = fetch_trechos_from_servers(all_servers)
    trechos_in_graph = create_graph(all_trechos)
    all_routes = create_routes(trechos_in_graph, origem, destino)
    return jsonify(all_routes), 200

# Endpoint para retornar trechos do servidor atual
@app.route('/return_trechos', methods=['GET'])
def return_trechos():
    trechos = load_trechos(filename)
    return jsonify(trechos), 200

# Endpoint para compra com controle de acesso a múltiplas regiões críticas
@app.route('/comprar', methods=['POST'])
def comprar():
    data = request.get_json()
    trecho_ids = data["trecho_ids"]  # Lista de IDs de trechos para a rota selecionada

    # Solicitar acesso a cada trecho (região crítica) na rota
    for trecho_id in trecho_ids:
        if not request_region_access(trecho_id, server_id, other_servers):
            return {"error": f"Falha ao adquirir acesso exclusivo para o trecho {trecho_id}"}, 409

    # Confirmar compra de todos os trechos adquiridos
    for trecho_id in trecho_ids:
        confirm_purchase(trecho_id, server_id, filename)

    return {"status": "confirmed", "message": f"Compra dos trechos {trecho_ids} confirmada"}, 200

# Endpoint para receber requisição de reserva de trecho de outro servidor
@app.route('/receive_request', methods=['POST'])
def receive_request_handler():
    data = request.get_json()
    receive_request(data)
    return {"status": "received"}, 200

if __name__ == "__main__":
    app.run(port=5001)
