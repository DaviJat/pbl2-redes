import requests
import json
import threading
import time

# URLs para cada servidor
SERVER_A_URL = "http://localhost:5000"
SERVER_B_URL = "http://localhost:5001"
TRECHO_ID = 1  # ID do trecho que os clientes tentarão reservar simultaneamente

def reserve_trecho(server_url, client_id):
    """Tenta reservar um trecho específico em um servidor e imprime o resultado."""
    print(f"Cliente {client_id} tentando reservar trecho {TRECHO_ID} em {server_url}")
    response = requests.post(f"{server_url}/reserve", json={"trecho_id": TRECHO_ID})
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "reserved":
            print(f"Cliente {client_id} reservou o trecho {TRECHO_ID} com sucesso em {server_url}")
        else:
            print(f"Cliente {client_id} falhou ao reservar trecho {TRECHO_ID} em {server_url}: {data['message']}")
    else:
        print(f"Erro na reserva pelo cliente {client_id} no servidor {server_url}")

# Função de teste para exclusão mútua
def test_exclusao_mutua():
    """Simula a tentativa de dois clientes reservando o mesmo trecho simultaneamente para testar exclusão mútua."""
    # Inicializa duas threads para simular os dois clientes em servidores diferentes
    client_a_thread = threading.Thread(target=reserve_trecho, args=(SERVER_A_URL, "A"))
    client_b_thread = threading.Thread(target=reserve_trecho, args=(SERVER_B_URL, "B"))

    # Inicia ambas as requisições quase simultaneamente
    client_a_thread.start()
    client_b_thread.start()

    # Aguarda ambas as threads terminarem
    client_a_thread.join()
    client_b_thread.join()

    # Verificação final se o trecho ainda está disponível
    print("Verificando estado final do trecho após as tentativas de reserva...")
    response_a = requests.get(f"{SERVER_A_URL}/trechos")
    response_b = requests.get(f"{SERVER_B_URL}/trechos")
    
    trechos_a = response_a.json() if response_a.status_code == 200 else []
    trechos_b = response_b.json() if response_b.status_code == 200 else []
    
    trecho_disponivel_a = any(t["id"] == TRECHO_ID for t in trechos_a)
    trecho_disponivel_b = any(t["id"] == TRECHO_ID for t in trechos_b)
    
    if not trecho_disponivel_a or not trecho_disponivel_b:
        print(f"O trecho {TRECHO_ID} foi reservado por um dos clientes, conforme esperado para exclusão mútua.")
    else:
        print(f"Erro: O trecho {TRECHO_ID} ainda está disponível nos dois servidores, exclusão mútua falhou.")

if __name__ == "__main__":
    test_exclusao_mutua()
