import re
from rotas import criar_grafo, obter_rotas_disponiveis, cidades, salvar_distancias, distancias

grafo = criar_grafo()
tickets = distancias

# Função que retorna o menu principal
def retorna_menu_principal():
    response = {
        "page_layout": [
            {"button": {"label": "Escolher destino", "method": "escolher_destino"}},
        ]
    }

    return response    

# Função que retorna o menu principal com dois dropdowns e um botão
def retorna_escolha_destino():
    response = {
        "page_layout": [
            {"dropdown": {"name": "origem", "label": "Escolha a origem", "options": cidades}},
            {"dropdown": {"name": "destino", "label": "Escolha o destino", "options": cidades}},
            {"button": {"label": "Enviar Seleções", "method": "trechos_disponiveis"}}
        ]
    }
    
    return response

# Função que retorna o menu principal
def retorna_lista_trechos():
    response = {
        "page_layout": [
            {"button": {"label": "Voltar", "method": "menu_principal"}}
        ]
    }

    return response

# Mostra 10 melhores trechos disponíveis para o cliente
def retorna_trechos_disponiveis(data):
    global grafo
    origem = data.get("origem")
    destino = data.get("destino")

    rotas_disponiveis = obter_rotas_disponiveis(grafo, origem, destino)

    response = {"page_layout": []}

    if rotas_disponiveis:
        rotas = []
        for i, (caminho, distancia, status) in enumerate(rotas_disponiveis, start=1):
            rota_str = f"{i}: {' -> '.join(caminho)} (Distância: {distancia} km) - {status}"
            rotas.append(rota_str)
        response["page_layout"].append({"dropdown": {"name": "rota", "label": "Escolha a rota", "options": rotas}})
        response["page_layout"].append({"button": {"label": "Comprar rota", "method": "comprar_rota"}})
    else:
        response["page_layout"].append({"message": "Nenhuma rota disponível."})

    response["page_layout"].append({"button": {"label": "Voltar", "method": "escolher_destino"}})

    return response

# Retorna confirmação de compra da rota selecionada
def retorna_confirmacao_rota(data):
    global grafo, tickets
    rota_selecionada = data.get("rota")  # Exemplo de formato: "3: Brasília -> Belo Horizonte -> Recife (Distância: 2830 km) - Disponível"

    # Extraindo a rota em formato de string e número da rota escolhida
    rota_str, status = rota_selecionada.split(" - ")
    cidades_match = re.search(r": (.+) \(Distância:", rota_str)
    caminho = cidades_match.group(1).split(" -> ")

    # Verificar se a rota ainda está disponível
    if "Disponível" in status:
        # Atualiza o número de passagens nas arestas do caminho escolhido
        for u, v in zip(caminho, caminho[1:]):
            if grafo[u][v]['tickets'] > 0:
                grafo[u][v]['tickets'] -= 1
                # Atualiza também o dicionário distancias para refletir a nova quantidade de passagens
                tickets[(u, v)] = (grafo[u][v]['weight'], grafo[u][v]['tickets'])
                if (v, u) in tickets:
                    tickets[(v, u)] = (grafo[u][v]['weight'], grafo[u][v]['tickets'])
                print(f"Passagens restantes no trecho {u} -> {v}: {grafo[u][v]['tickets']}")
            else:
                # Resposta de falha ao comprar rota não mais disponível
                response = {
                    "page_layout": [
                        {"message": "Compra negada, rota indisponível. Por favor, escolha outra rota."},
                        {"button": {"label": "Escolher outro destino", "method": "escolher_destino"}}
                    ]
                }

                return response

        # Salva o estado atualizado das passagens no arquivo
        salvar_distancias(tickets)
        # Resposta de confirmação de compra
        response = {
            "page_layout": [
                {"message": "Compra confirmada. Parabéns! Sua rota foi adquirida com sucesso."},
                {"button": {"label": "Voltar ao Menu Principal", "method": "menu_principal"}}
            ]
        }
    else:
        # Resposta de falha ao escolher uma rota indisponivel
        response = {
            "page_layout": [
                {"message": "Rota escolhida não indisponível. Por favor, escolha outra rota."},
                {"button": {"label": "Escolher outro destino", "method": "escolher_destino"}}
            ]
        }

    return response
