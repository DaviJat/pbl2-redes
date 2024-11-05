import os
import pickle
import threading
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import create_routes, fetch_trechos_from_servers, load_trechos, create_graph

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
    trechos = request.get_json()
    print(trechos) #

    return 'Compra'

if __name__ == "__main__":
    app.run(port=5001)
