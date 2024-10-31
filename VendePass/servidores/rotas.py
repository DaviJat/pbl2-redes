import networkx as nx
import pickle
import os

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
    ('Rio de Janeiro', 'Porto Alegre'): (1550, 2),
    ('Brasília', 'Salvador'): (1440, 6),
    ('Brasília', 'Fortaleza'): (2200, 2),
    ('Brasília', 'Belo Horizonte'): (740, 7),
    ('Brasília', 'Manaus'): (3490, 1),
    ('Brasília', 'Curitiba'): (1370, 5),
    ('Brasília', 'Recife'): (2200, 3),
    ('Brasília', 'Porto Alegre'): (2020, 4),
    ('Salvador', 'Fortaleza'): (1020, 3),
    ('Salvador', 'Belo Horizonte'): (1370, 6),
    ('Salvador', 'Manaus'): (4430, 2),
    ('Salvador', 'Curitiba'): (2290, 4),
    ('Salvador', 'Recife'): (800, 5),
    ('Salvador', 'Porto Alegre'): (3070, 2),
    ('Fortaleza', 'Belo Horizonte'): (2520, 3),
    ('Fortaleza', 'Manaus'): (5680, 1),
    ('Fortaleza', 'Curitiba'): (3680, 2),
    ('Fortaleza', 'Recife'): (800, 6),
    ('Fortaleza', 'Porto Alegre'): (4570, 1),
    ('Belo Horizonte', 'Manaus'): (3930, 2),
    ('Belo Horizonte', 'Curitiba'): (1000, 4),
    ('Belo Horizonte', 'Recife'): (2090, 3),
    ('Belo Horizonte', 'Porto Alegre'): (1710, 5),
    ('Manaus', 'Curitiba'): (4360, 1),
    ('Manaus', 'Recife'): (5900, 1),
    ('Manaus', 'Porto Alegre'): (4900, 1),
    ('Curitiba', 'Recife'): (3030, 2),
    ('Curitiba', 'Porto Alegre'): (710, 7),
    ('Recife', 'Porto Alegre'): (3700, 2),
}

# Verificar se o arquivo de distâncias existe e carregar ou inicializar
distancias = carregar_distancias()
if distancias is None:
    distancias = distancias_default
    salvar_distancias(distancias)

grafo = nx.Graph()

# Criar o grafo
def criar_grafo():
    global grafo
    for (cidade1, cidade2), (distancia, passagens) in distancias.items():
        grafo.add_edge(cidade1, cidade2, weight=distancia, tickets=passagens)
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




