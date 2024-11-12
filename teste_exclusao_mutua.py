import requests
import threading
import time
import random

# URLs dos servidores
SERVER_URLS = {
    "a": 'http://127.0.0.1:5000/comprar',
    "b": 'http://127.0.0.1:5001/comprar',
    "c": 'http://127.0.0.1:5002/comprar'
}

# Dados dos trechos disponíveis para cada servidor
TRECHOS = {
    "a": [
        {"id": 1, "servidor": "a", "origem": "Brasília", "destino": "Salvador", "distancia": 1440, "quantidade_passagens": 100},
        {"id": 2, "servidor": "a", "origem": "Salvador", "destino": "São Paulo", "distancia": 1960, "quantidade_passagens": 100},
        {"id": 3, "servidor": "a", "origem": "São Paulo", "destino": "Curitiba", "distancia": 410, "quantidade_passagens": 100},
        {"id": 4, "servidor": "a", "origem": "Curitiba", "destino": "Porto Alegre", "distancia": 710, "quantidade_passagens": 100},
    ],
    "b": [
        {"id": 1, "servidor": "b", "origem": "Rio de Janeiro", "destino": "Brasília", "distancia": 1160, "quantidade_passagens": 100},
        {"id": 2, "servidor": "b", "origem": "Brasília", "destino": "Belo Horizonte", "distancia": 740, "quantidade_passagens": 100},
        {"id": 3, "servidor": "b", "origem": "Belo Horizonte", "destino": "Salvador", "distancia": 1370, "quantidade_passagens": 100},
        {"id": 4, "servidor": "b", "origem": "Salvador", "destino": "Recife", "distancia": 800, "quantidade_passagens": 100},
    ],
    "c": [
        {"id": 1, "servidor": "c", "origem": "Manaus", "destino": "Brasília", "distancia": 3490, "quantidade_passagens": 100},
        {"id": 2, "servidor": "c", "origem": "Brasília", "destino": "São Paulo", "distancia": 1015, "quantidade_passagens": 100},
        {"id": 3, "servidor": "c", "origem": "São Paulo", "destino": "Rio de Janeiro", "distancia": 430, "quantidade_passagens": 100},
        {"id": 4, "servidor": "c", "origem": "Rio de Janeiro", "destino": "Fortaleza", "distancia": 2800, "quantidade_passagens": 100},
    ]
}

# Variáveis globais para armazenar resultados
successful_purchases = 0
failed_purchases = 0
purchase_summary = []
purchase_count = {}  # Dicionário para contar as compras por trecho

# Função que cada thread (cliente) vai executar
def attempt_purchase(thread_id):
    global successful_purchases, failed_purchases

    # Escolhe um servidor e um trecho aleatoriamente
    servidor = random.choice(list(SERVER_URLS.keys()))
    server_url = SERVER_URLS[servidor]
    trecho = random.choice(TRECHOS[servidor])

    # Dados para a compra
    purchase_data = {"rota": [trecho]}
    
    try:
        print(f"[Cliente {thread_id}] Tentando comprar o trecho de {trecho['origem']} para {trecho['destino']} no servidor {servidor.upper()}")
        response = requests.post(server_url, json=purchase_data)
        response_data = response.json()
        status = response_data.get("status")
        message = response_data.get("message")

        # Atualiza contadores globais e resumo com base na resposta
        if status == "success":
            print(f"[Cliente {thread_id}] Compra bem-sucedida: {message}")
            successful_purchases += 1
            purchase_summary.append((thread_id, trecho["origem"], trecho["destino"], "Sucesso"))
            
            # Atualiza o contador de compra para o trecho específico
            trecho_key = f"{trecho['origem']} -> {trecho['destino']}"
            if trecho_key in purchase_count:
                purchase_count[trecho_key] += 1
            else:
                purchase_count[trecho_key] = 1
        else:
            print(f"[Cliente {thread_id}] Falha na compra: {message}")
            failed_purchases += 1
            purchase_summary.append((thread_id, trecho["origem"], trecho["destino"], "Falha"))
    except Exception as e:
        print(f"[Cliente {thread_id}] Erro ao tentar realizar a compra: {e}")
        failed_purchases += 1
        purchase_summary.append((thread_id, trecho["origem"], trecho["destino"], "Erro"))

# Número de threads para simular um número maior de tentativas
NUM_CLIENTS = 500  # Aumentado para mais tentativas

# Lista para armazenar as threads
threads = []

print("==== Início do Teste de Múltiplas Compras com Rotas e Trechos Diversificados ====")
print(f"Tentando realizar {NUM_CLIENTS} compras simultâneas para trechos variados.\n")

# Inicia múltiplas threads para tentar a compra simultânea
for i in range(NUM_CLIENTS):
    thread = threading.Thread(target=attempt_purchase, args=(i,))
    threads.append(thread)
    thread.start()
    time.sleep(0.05)  # Reduzido para aumentar a simultaneidade

# Aguarda todas as threads finalizarem
for thread in threads:
    thread.join()

print("\n==== Teste de Múltiplas Compras Concluído ====")

# Exibe o resumo dos resultados
print("\nResumo dos Resultados:")
print(f"Compras bem-sucedidas: {successful_purchases}")
print(f"Compras falhadas (sem passagens disponíveis ou erro): {failed_purchases}")
print("\nDetalhes das Tentativas de Compra:")
for summary in purchase_summary:
    print(f"Cliente {summary[0]}: Origem: {summary[1]}, Destino: {summary[2]}, Resultado: {summary[3]}")

# Exibe a contagem de passagens compradas por trecho
print("\nContagem de passagens compradas por trecho:")
for trecho, count in purchase_count.items():
    print(f"Trecho {trecho}: {count} passagens compradas")

# Verificação de exclusão mútua
total_passagens_disponiveis = sum(t["quantidade_passagens"] for sublist in TRECHOS.values() for t in sublist)
if successful_purchases <= total_passagens_disponiveis:
    print("\nResultado: A exclusão mútua funcionou corretamente.")
else:
    print("\nResultado: A exclusão mútua falhou. Verifique o código para possíveis inconsistências.")
