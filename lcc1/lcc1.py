from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Lista de voos da LCC 1
flights_lcc1 = [
    {'id': 1, 'origin': 'São Paulo', 'destination': 'Rio de Janeiro', 'price': 150},
    {'id': 2, 'origin': 'Salvador', 'destination': 'Fortaleza', 'price': 200}
]

# Página inicial com o botão
@app.route('/')
def index():
    return render_template('index.html')

# Página para exibir os voos
@app.route('/voos', methods=['GET'])
def show_flights():
    all_flights = flights_lcc1.copy()

    try:
        # Consulta os voos do Servidor 2
        response = requests.get(f"http://127.0.0.1:5002/api/flights")
        all_flights.extend(response.json())
    except requests.exceptions.RequestException as e:
        print('Não foi possível recuperar rotas do servidor 2')

    try:
        # Consulta os voos do Servidor 3
        response = requests.get(f"http://127.0.0.1:5003/api/flights")
        all_flights.extend(response.json())
    except requests.exceptions.RequestException as e:
        print('Não foi possível recuperar rotas do servidor 3')

    # Redireciona para a página voos.html passando a lista de voos
    return render_template('voos.html', flights=all_flights)

# API para retornar os voos disponíveis da LCC 1
@app.route('/api/flights', methods=['GET'])
def get_flights():
    return jsonify(flights_lcc1)

if __name__ == '__main__':
    app.run(port=5001)
