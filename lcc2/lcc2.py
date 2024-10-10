from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Lista de voos da LCC 2
flights_lcc2 = [
    {'id': 3, 'origin': 'Belo Horizonte', 'destination': 'Brasília', 'price': 180},
    {'id': 4, 'origin': 'Porto Alegre', 'destination': 'Curitiba', 'price': 220}
]

# Página inicial com o botão
@app.route('/')
def index():
    return render_template('index.html')

# Página para exibir os voos
@app.route('/voos', methods=['GET'])
def show_flights():
    all_flights = flights_lcc2.copy()

    try:
        # Consulta os voos do Servidor 1
        response = requests.get(f"http://127.0.0.1:5001/api/flights")
        all_flights.extend(response.json())
    except requests.exceptions.RequestException as e:
        print('Não foi possível recuperar rotas do servidor 1')

    try:
        # Consulta os voos do Servidor 3
        response = requests.get(f"http://127.0.0.1:5003/api/flights")
        all_flights.extend(response.json())
    except requests.exceptions.RequestException as e:
        print('Não foi possível recuperar rotas do servidor 3')

    # Redireciona para a página voos.html passando a lista de voos
    return render_template('voos.html', flights=all_flights)

# API para retornar os voos disponíveis da LCC 2
@app.route('/api/flights', methods=['GET'])
def get_flights():
    return jsonify(flights_lcc2)

if __name__ == '__main__':
    app.run(port=5002)
