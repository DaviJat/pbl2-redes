import pickle
import os

# Diretórios e nomes de arquivos de cada servidor
base_diretorio = "project"
arquivos_rotas = {
    "Server A": os.path.join(base_diretorio, "server_a", "trechos_server_a.plk"),
    "Server B": os.path.join(base_diretorio, "server_b", "trechos_server_b.plk"),
    "Server C": os.path.join(base_diretorio, "server_c", "trechos_server_c.plk"),
}

def carregar_e_printar_rotas():
    for servidor, caminho_arquivo in arquivos_rotas.items():
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, 'rb') as f:
                rotas = pickle.load(f)
                print(f"\n--- {servidor} ---")
                for rota in rotas:
                    print(rota)
        else:
            print(f"\n[ERRO] Arquivo não encontrado para {servidor}: {caminho_arquivo}")

if __name__ == "__main__":
    carregar_e_printar_rotas()
