from flask import Flask, request, jsonify
from utils import request_reservation, receive_request, confirm_reservation, load_trechos

app = Flask(__name__)

# Identificação do servidor e arquivo JSON de trechos
server_id = "C"
filename = "trechos_server_c.json"
other_servers = ["http://localhost:5000", "http://localhost:5001"]

# Carregar os trechos deste servidor
trechos = load_trechos(filename)

# Endpoint para obter trechos disponíveis
@app.route('/trechos', methods=['GET'])
def get_trechos():
    return jsonify(trechos), 200

# Endpoint para enviar solicitação de reserva
@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    trecho_id = data["trecho_id"]
    trecho = next((t for t in trechos if t["id"] == trecho_id), None)
    
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
    app.run(port=5002)
