import requests
import threading
import time

# URL do servidor A
SERVER_URL = 'http://127.0.0.1:5000/comprar'

# Dados da rota para a compra (todos os clientes vão tentar comprar o mesmo trecho)
purchase_data = {
    "rota": [
        {
            "id": 1,
            "servidor": "a",
            "origem": "São Paulo",
            "destino": "Rio de Janeiro",
            "distancia": 430,
            "quantidade_passagens": 10
        }
    ]
}

# Variáveis globais para armazenar resultados
successful_purchases = 0
failed_purchases = 0

# Função que cada thread (cliente) vai executar
def attempt_purchase(thread_id):
    global successful_purchases, failed_purchases
    try:
        print(f"[Cliente {thread_id}] Tentando comprar o trecho...")
        response = requests.post(SERVER_URL, json=purchase_data)
        response_data = response.json()
        status = response_data.get("status")
        message = response_data.get("message")
        
        # Atualiza contadores globais com base na resposta
        if status == "success":
            print(f"[Cliente {thread_id}] Compra bem-sucedida: {message}")
            successful_purchases += 1
        else:
            print(f"[Cliente {thread_id}] Falha na compra: {message}")
            failed_purchases += 1
    except Exception as e:
        print(f"[Cliente {thread_id}] Erro ao tentar realizar a compra: {e}")
        failed_purchases += 1

# Número de threads para simular múltiplos clientes
NUM_CLIENTS = 12

# Lista para armazenar as threads
threads = []

print("==== Início do Teste de Múltiplas Compras ====")
print(f"Tentando realizar {NUM_CLIENTS} compras simultâneas para o mesmo trecho.\n")

# Inicia múltiplas threads para tentar a compra simultânea
for i in range(NUM_CLIENTS):
    thread = threading.Thread(target=attempt_purchase, args=(i,))
    threads.append(thread)
    thread.start()
    time.sleep(0.1)  # Atraso pequeno para simular solicitações quase simultâneas

# Aguarda todas as threads finalizarem
for thread in threads:
    thread.join()

print("\n==== Teste de Múltiplas Compras Concluído ====")

# Exibe o resumo dos resultados
print("\nResumo dos Resultados:")
print(f"Compras bem-sucedidas: {successful_purchases}")
print(f"Compras falhadas (sem passagens disponíveis): {failed_purchases}")

# Verificação do resultado
if successful_purchases == 10 and failed_purchases == 2:
    print("\nResultado: A exclusão mútua funcionou corretamente. Apenas dez compras foram permitidas.")
else:
    print("\nResultado: A exclusão mútua falhou. Verifique o código para possíveis inconsistências.")
