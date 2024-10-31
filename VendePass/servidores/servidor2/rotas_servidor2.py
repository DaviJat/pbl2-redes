import networkx as nx
import pickle
import os
from servidor2 import retornar_distancia_servidor_1, retornar_distancia_servidor_3

# Definir as cidades brasileiras
cidades = ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza',
           'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre']

# Caminho para o arquivo de distâncias
arquivo_distancias = "distancias.plk"


# Função para salvar as distâncias no arquivo
def salvar_distancias(distancias):
    with open(arquivo_distancias, 'wb') as arquivo:
        pickle.dump(distancias, arquivo)


# Função para carregar as distâncias do arquivo
def carregar_distancias():
    if os.path.exists(arquivo_distancias):
        with open(arquivo_distancias, 'rb') as arquivo:
            return pickle.load(arquivo)
    else:
        return None


# Definir as distâncias reais entre as cidades (em km) e a quantidade de passagens disponíveis por trecho
distancias_default = {
    ('São Paulo', 'Rio de Janeiro'): (430, 10),
    ('São Paulo', 'Brasília'): (1015, 5),
    ('São Paulo', 'Salvador'): (1960, 3),
    ('São Paulo', 'Fortaleza'): (3120, 2),
    ('São Paulo', 'Belo Horizonte'): (585, 8),
    ('São Paulo', 'Manaus'): (3930, 4),
    ('São Paulo', 'Curitiba'): (410, 6),
    ('São Paulo', 'Recife'): (2670, 2),
    ('São Paulo', 'Porto Alegre'): (1115, 5),
    ('Rio de Janeiro', 'Brasília'): (1160, 6),
    ('Rio de Janeiro', 'Salvador'): (1660, 4),
    ('Rio de Janeiro', 'Fortaleza'): (2800, 1),
    ('Rio de Janeiro', 'Belo Horizonte'): (440, 7),
    ('Rio de Janeiro', 'Manaus'): (3680, 3),
    ('Rio de Janeiro', 'Curitiba'): (850, 5),
    ('Rio de Janeiro', 'Recife'): (2330, 3),
}

# Verificar se o arquivo de distâncias existe e carregar ou inicializar
distancias = carregar_distancias()
if distancias is None:
    distancias = distancias_default
    salvar_distancias(distancias)

distancias_servidor1 = retornar_distancia_servidor_1()
distancias_servidor3 = retornar_distancia_servidor_3()

grafo = nx.Graph()


# Criar o grafo
def criar_grafo():
    global grafo
    for (cidade1, cidade2), (distancia, passagens) in distancias.items():
        grafo.add_edge(cidade1, cidade2, weight=distancia, tickets=passagens)

    if distancias_servidor1:
        for (cidade1, cidade2), (distancia, tickets) in distancias_servidor1.items():
            if (cidade1, cidade2) not in grafo.edges:
                grafo.add_edge(cidade1, cidade2, weight=distancia, tickets=tickets)

    if distancias_servidor3:
        for (cidade1, cidade2), (distancia, tickets) in distancias_servidor3.items():
            if (cidade1, cidade2) not in grafo.edges:
                grafo.add_edge(cidade1, cidade2, weight=distancia, tickets=tickets)

    return grafo


def obter_rotas_disponiveis(grafo, cidade_origem, cidade_destino):
    caminhos_possiveis = []

    if cidade_origem == cidade_destino:
        return caminhos_possiveis

    def dfs(atual, destino, caminho_atual, visitados):
        if atual == destino:
            caminhos_possiveis.append(caminho_atual.copy())
            return

        visitados.add(atual)  # Marca a cidade como visitada
        for vizinho in grafo[atual]:
            if vizinho not in visitados:  # Verifica se não revisita
                caminho_atual.append(vizinho)
                dfs(vizinho, destino, caminho_atual, visitados)
                caminho_atual.pop()  # Volta para o caminho anterior
        visitados.remove(atual)  # Remove a cidade do conjunto de visitados

    # Inicializa a busca
    dfs(cidade_origem, cidade_destino, [cidade_origem], set())

    # Processar as rotas
    rotas_resultantes = []
    for path in caminhos_possiveis:
        passagens_disponiveis = all(grafo[u][v]['tickets'] > 0 for u, v in zip(path, path[1:]))
        distancia = sum(grafo[u][v]['weight'] for u, v in zip(path, path[1:]))
        status = "Disponível" if passagens_disponiveis else "Indisponível"
        rotas_resultantes.append((path, distancia, status))

    # Ordena e limita as rotas para as 10 melhores
    rotas_resultantes.sort(key=lambda x: x[1])  # Ordena por distância
    return rotas_resultantes[:10]  # Retorna apenas as 10 melhores rotas




