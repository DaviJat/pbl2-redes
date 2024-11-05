import requests
import concurrent.futures
import time
import copy

API_URL = 'http://127.0.0.1:5000'  # URL da API

# Exemplo de uma rota que será usada para simular a compra
ROTA_EXEMPLO = {
    "rota": [
        {
            "id": 1,
            "servidor": "a",
            "origem": "São Paulo",
            "destino": "Rio de Janeiro",
            "distancia": 430,
            "quantidade_passagens": 1
        }
    ]
}

def comprar_rota(rota):
    """
    Função para simular a compra de uma rota.
    Envia uma requisição POST para a API e retorna o resultado.
    """
    rota_payload = copy.deepcopy(rota)  # Garante que cada thread use uma cópia do JSON
    print("Tentando comprar a rota com dados:", rota_payload)
    try:
        response = requests.post(f"{API_URL}/comprar", json=rota_payload)
        
        if response.ok:
            data = response.json()
            if data.get("status") == "success":
                print("Compra bem-sucedida:", data)
            else:
                print("Compra falhou. Motivo:", data.get("message", "Erro desconhecido"))
        else:
            # Exibe o conteúdo da resposta para diagnósticos de erro
            print(f"Erro ao tentar comprar a rota. Status: {response.status_code}, Detalhes: {response.text}")
        
        return response.ok
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return False

def testar_compras_concorrentes(rota, tentativas=5):
    """
    Função para testar múltiplas compras concorrentes de uma mesma rota.
    Utiliza um executor de threads para simular compras simultâneas.
    """
    print("Iniciando o teste de exclusão mútua com múltiplas tentativas de compra...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=tentativas) as executor:
        # Dispara várias threads para comprar a mesma rota simultaneamente
        resultados = list(executor.map(comprar_rota, [rota] * tentativas))
    
    # Verifica o número de compras bem-sucedidas
    compras_bem_sucedidas = sum(resultados)
    print(f"\nTotal de compras bem-sucedidas: {compras_bem_sucedidas}")
    print(f"Total de tentativas: {tentativas}")
    
    # Avalia o resultado do teste
    if compras_bem_sucedidas == 1:
        print("Exclusão mútua está funcionando corretamente. Apenas uma compra foi permitida.")
    else:
        print("Falha na exclusão mútua! Mais de uma compra foi realizada para a mesma rota.")

# Executa o teste
if __name__ == "__main__":
    # Espera um breve momento para garantir que a API esteja ativa
    time.sleep(1)
    testar_compras_concorrentes(ROTA_EXEMPLO, tentativas=5)
