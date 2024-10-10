from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Lista de voos da LCC 3
flights_lcc3 = [
    {'id': 5, 'origin': 'Recife', 'destination': 'Natal', 'price': 170},
    {'id': 6, 'origin': 'Manaus', 'destination': 'Belém', 'price': 230}
]

# Página inicial com o botão
@app.route('/')
def index():
    return render_template('index.html')

# Página para exibir os voos
@app.route('/voos', methods=['GET'])
def show_flights():
    all_flights = flights_lcc3.copy()

    try:
        # Consulta os voos do Servidor 1
        response = requests.get(f"http://127.0.0.1:5001/api/flights")
        all_flights.extend(response.json())
    except requests.exceptions.RequestException as e:
        print('Não foi possível recuperar rotas do servidor 1')

    try:
        # Consulta os voos do Servidor 2
        response = requests.get(f"http://127.0.0.1:5002/api/flights")
        all_flights.extend(response.json())
    except requests.exceptions.RequestException as e:
        print('Não foi possível recuperar rotas do servidor 2')

    # Redireciona para a página voos.html passando a lista de voos
    return render_template('voos.html', flights=all_flights)

# API para retornar os voos disponíveis da LCC 3
@app.route('/api/flights', methods=['GET'])
def get_flights():
    return jsonify(flights_lcc3)

if __name__ == '__main__':
    app.run(port=5003)
