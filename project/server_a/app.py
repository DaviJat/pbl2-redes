import os
from flask import Flask, request, jsonify
from flask_cors import CORS 
import pickle
from utils import create_routes, fetch_trechos_from_servers, request_reservation, receive_request, confirm_reservation, load_trechos, create_graph

app = Flask(__name__)
CORS(app)

# Identificação do servidor e arquivo pickle de trechos
server_id = "A"
filename = os.path.join("project", "server_a", "trechos_server_a.plk")  
other_servers = ["http://localhost:5001", "http://localhost:5002"]

# Carregar os trechos deste servidor
def load_trechos(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

@app.route('/trechos', methods=['GET'])
def get_trechos():
    origem = request.args.get('origem', '')
    destino = request.args.get('destino', '')
    all_servers = [f"http://127.0.0.1:5000"] + other_servers
    all_trechos = fetch_trechos_from_servers(all_servers)
    trechos_in_graph = create_graph(all_trechos)
    all_routes = create_routes(trechos_in_graph, origem, destino)
    print(all_routes)

    return jsonify(all_routes), 200

# Endpoint para retornar trechos do servidor atual
@app.route('/return_trechos', methods=['GET'])
def return_trechos():
    trechos = load_trechos(filename)
    return jsonify(trechos), 200

# Endpoint para enviar solicitação de reserva
@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    trecho_id = data["trecho_id"]
    trecho = next((t for t in load_trechos(filename) if t["id"] == trecho_id), None)
    
    if trecho:
        request_reservation(trecho, server_id, other_servers)
        return {"status": "requested"}, 200
    return {"error": "Trecho não encontrado"}, 404

# Endpoint para receber solicitação de reserva de outro servidor
@app.route('/receive_request', methods=['POST'])
def receive_request_handler():
    data = request.get_json()
    receive_request(data)
    return {"status": "received"}, 200

# Endpoint para confirmar compra do trecho
@app.route('/confirm_purchase', methods=['POST'])
def confirm_purchase():
    data = request.get_json()
    trecho_id = data["trecho_id"]
    confirm_reservation(trecho_id, server_id, filename)
    return {"status": "confirmed"}, 200

if __name__ == "__main__":
    app.run(port=5000)
