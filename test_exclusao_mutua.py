import threading
import time
import requests

# URLs dos servidores
server_urls = {
    "A": "http://127.0.0.1:5000",
    "B": "http://127.0.0.1:5001",
    "C": "http://127.0.0.1:5002"
}

# Definir rotas a serem compradas por cada servidor
# Cada servidor irá tentar comprar trechos em comum para testar a exclusão mútua
routes_to_purchase = {
    "A": {"trecho_ids": [1, 10]},  # São Paulo -> Rio de Janeiro, Rio de Janeiro -> Brasília
    "B": {"trecho_ids": [10, 2]},  # Rio de Janeiro -> Brasília, Brasília -> Salvador
    "C": {"trecho_ids": [10, 8]}   # Rio de Janeiro -> Brasília, Brasília -> Porto Alegre
}

# Função para comprar uma rota em um servidor específico
def purchase_route(server_id):
    try:
        url = f"{server_urls[server_id]}/comprar"
        response = requests.post(url, json=routes_to_purchase[server_id])
        print(f"Servidor {server_id}: {response.json()}")
    except Exception as e:
        print(f"Erro ao tentar comprar rota no servidor {server_id}: {e}")

# Função principal para rodar os testes de compra de rotas
def main():
    # Threads para simular compras simultâneas nos três servidores
    threads = []
    for server_id in server_urls:
        thread = threading.Thread(target=purchase_route, args=(server_id,))
        threads.append(thread)
        thread.start()

    # Esperar todas as threads terminarem
    for thread in threads:
        thread.join()

# Executar o teste
if __name__ == "__main__":
    print("Iniciando teste de compra de rotas simultâneas nos servidores A, B e C.")
    main()
    print("Teste concluído.")
