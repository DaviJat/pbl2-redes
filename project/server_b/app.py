# app.py

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
server_id = "B"  # Identificação do servidor atual
locks = {} # Dicionário de locks para cada trecho
filename = os.path.join("project", "server_b", "trechos_server_b.plk")  # Caminho do arquivo de dados
other_servers = ["http://localhost:5000", "http://localhost:5002"]  # URLs dos outros servidores

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
    # Rota para obter trechos de todos os servidores e criar rotas de viagem
    origem = request.args.get('origem', '')  # Origem da rota
    destino = request.args.get('destino', '')  # Destino da rota
    all_servers = ["http://127.0.0.1:5001"] + other_servers  # Lista de todos os servidores

    print(f"Obtendo trechos dos servidores: {all_servers}")  # Log dos servidores consultados

    # Coleta de trechos e criação de rotas
    all_trechos = fetch_trechos_from_servers(all_servers)
    trechos_in_graph = create_graph(all_trechos)
    all_routes = create_routes(trechos_in_graph, origem, destino)

    return jsonify(all_routes), 200  # Retorna as rotas como JSON

@app.route('/return_trechos', methods=['GET'])
def return_trechos():
    # Rota para retornar todos os trechos disponíveis neste servidor
    trechos = load_trechos(filename)  # Carrega trechos do arquivo local
    return jsonify(trechos), 200  # Retorna os trechos como JSON

@app.route('/comprar', methods=['POST'])
def comprar():
    """Rota para processar uma compra de trecho com controle de bloqueio."""
    data = request.get_json()  # Dados dos trechos para compra
    print(f"Recebido pedido de compra: {data}")
    
    try:
        # Adquire o lock de todos os trechos antes de realizar a compra
        for trecho in data["rota"]:
            trecho_id = trecho["id"]
            trecho_lock = acquire_lock(trecho_id)
            trecho_lock.acquire()  # Bloqueia o trecho específico

        # Processa a compra enquanto os trechos estão bloqueados
        request_purchase(data, other_servers)
        
        # Libera todos os locks após o processamento
        for trecho in data["rota"]:
            trecho_id = trecho["id"]
            locks[trecho_id].release()

        return jsonify({"status": "success", "message": "Compra realizada com sucesso"}), 200
    except Exception as e:
        print(f"Erro ao processar compra: {e}")
        # Libera os locks em caso de erro
        for trecho in data["rota"]:
            trecho_id = trecho["id"]
            if locks[trecho_id].locked():
                locks[trecho_id].release()
        return jsonify({"status": "error", "message": "Erro ao realizar a compra"}), 500


@app.route('/purchase_request', methods=['POST'])
def receive_purchase_request():
    # Rota para receber uma solicitação de compra com controle de exclusão mútua
    global clock, queue
    data = request.get_json()  # Dados da requisição de compra

    if not data:  # Valida dados
        return jsonify({"error": "Invalid data"}), 400

    # Atualiza o clock e adiciona requisição à fila
    clock = max(clock, data["id"]) + 1
    queue.append(data)
    print(f"Requisição de compra recebida de {data['server_id']} com timestamp {data['id']}")  # Log da requisição

    return jsonify({"message": "Compra request received", "clock": clock}), 200

@app.route('/release', methods=['POST'])
def receive_release():
    # Rota para liberar acesso à seção crítica após conclusão de compra
    global queue
    data = request.get_json()  # Dados da liberação

    if not data:  # Valida dados
        return jsonify({"error": "Invalid data"}), 400

    # Remove a requisição da fila
    queue = [req for req in queue if not (req["id"] == data["id"] and req["server_id"] == data["server_id"])]
    print(f"Liberação recebida de {data['server_id']} para timestamp {data['id']}")  # Log da liberação

    return jsonify({"message": "Release received"}), 200

@app.route('/update_trecho', methods=['POST'])
def update_trecho():
    # Rota para atualizar a quantidade de passagens disponíveis em um trecho específico
    trecho_data = request.get_json()  # Dados do trecho a ser atualizado
    trecho_id = trecho_data["id"]  # ID do trecho
    trecho_servidor = trecho_data["servidor"]  # Servidor do trecho

    # Carrega trechos existentes
    trechos = load_trechos(filename)

    # Busca e atualiza o trecho correspondente
    for trecho in trechos:
        if trecho["id"] == trecho_id and trecho["servidor"] == trecho_servidor:
            if trecho["quantidade_passagens"] > 1:
                trecho["quantidade_passagens"] -= 1
                print(f"Atualizado trecho: {trecho}")  # Log da atualização
            else:
                trechos.remove(trecho)  # Remove trecho se não há passagens
                print(f"Removido trecho por falta de passagens: {trecho}")  # Log da remoção

            # Salva o estado atualizado no arquivo
            with open(filename, 'wb') as f:
                pickle.dump(trechos, f)

            return jsonify({"message": "Trecho atualizado com sucesso"}), 200

    return jsonify({"error": "Trecho não encontrado"}), 404  # Caso o trecho não seja encontrado

if __name__ == "__main__":
    app.run(port=5001)  # Inicia o servidor Flask na porta 5001
