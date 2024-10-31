import tkinter as tk
from tkinter import messagebox
import socket
import json

# Função para limpar a janela do navegador
def limpar_navegador(navegador):
    for widget in navegador.winfo_children():
        widget.destroy()

# Função para enviar a requisição para o servidores
def enviar_requisicao(method, data):
    try:
        # Gera a requisição a ser enviada para o servidores
        request = {
            "method": method,
            "data": data
        }

        # Dicionário para armazenar dados da requisição
        data_request = {}

        # Abre o socket de conexão e envia a requisição
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, int(SERVER_PORT)))
        client_socket.send(json.dumps(request).encode("utf-8"))

        # Recebe resposta do cliente
        server_response = client_socket.recv(8192).decode('utf-8')
        response = json.loads(server_response)

        # Verifica se o servidores enviou um layout de página para renderizar
        page_layout = response.get("page_layout", "")
        if page_layout != "":
            limpar_navegador(navegador)
            for item in page_layout:
                if "dropdown" in item:
                    dropdown_info = item["dropdown"]

                    label = tk.Label(navegador, text=dropdown_info["label"])
                    label.pack(pady=5)

                    # Variável que armazena o valor selecionado no dropdown (uma instância para cada dropdown)
                    numero_selecionado = tk.StringVar(navegador)
                    numero_selecionado.set(dropdown_info["options"][0])

                    # Função para atualizar o data_request para cada dropdown
                    def atualizar_data_request(dropdown_name, numero_selecionado_var):
                        def inner(*args):
                            valor_selecionado = numero_selecionado_var.get()
                            data_request[dropdown_name] = valor_selecionado
                        return inner

                    # Adiciona um trace para chamar a função quando o valor mudar, agora usando a variável correta
                    numero_selecionado.trace("w", atualizar_data_request(dropdown_info["name"], numero_selecionado))

                    option_menu = tk.OptionMenu(navegador, numero_selecionado, *dropdown_info["options"])
                    option_menu.pack(pady=5)

                    # Inicializa o valor no data_request
                    data_request[dropdown_info["name"]] = numero_selecionado.get()
                    
                if "button" in item:
                    button_data = item["button"]
                    button_label = button_data["label"]
                    button_method = button_data["method"]
                    tk.Button(navegador, text=button_label, command=lambda method=button_method, data=data_request: enviar_requisicao(method, data)).pack(pady=10)

                if "message" in item:
                    message_label = item["message"]
                    tk.Label(navegador, text=message_label).pack(pady=10)

        client_socket.close()
    except:
        limpar_navegador(navegador)
        button_label = "Erro na conexão, voltar ao navegador"
        tk.Button(navegador, text=button_label, command=lambda reiniciar=True : iniciar_navegador(reiniciar)).pack(pady=10)

# Função de conexão ao servidores
def iniciar_conexao():
    ip = ip_entry.get()
    port = port_entry.get()
    
    # Validações
    if not ip:
        messagebox.showerror("Erro", "Você deve inserir o IP do servidores!")
    elif not port:
        messagebox.showerror("Erro", "Você deve inserir a porta do servidores!")
    else:
        # Limpa a janela
        limpar_navegador(navegador)
        global SERVER_IP, SERVER_PORT
        SERVER_IP, SERVER_PORT = ip, port

        method = "menu_principal"
        data = {}

        # Solicita o menu principal para mostrar ao usuário
        enviar_requisicao(method, data)

# Função para iniciar o navegador
def iniciar_navegador(reiniciar=False):
    global navegador, ip_entry, port_entry, SERVER_IP, SERVER_PORT

    # Limpar o navegador anterior, caso seja um reinício
    if reiniciar:
        navegador.destroy()

    # Criação da janela principal
    navegador = tk.Tk()
    navegador.title("Navegador")

    SERVER_IP, SERVER_PORT = None, None

    # Campo para IP do servidores
    tk.Label(navegador, text="IP do servidores:").grid(row=0, column=0, padx=10, pady=10)
    ip_entry = tk.Entry(navegador)
    ip_entry.grid(row=0, column=1, padx=10, pady=10)

    # Campo para porta do servidores
    tk.Label(navegador, text="Porta do servidores:").grid(row=1, column=0, padx=10, pady=10)
    port_entry = tk.Entry(navegador)
    port_entry.grid(row=1, column=1, padx=10, pady=10)

    # Botão para conectar ao servidores
    connect_button = tk.Button(navegador, text="Conectar", command=iniciar_conexao)
    connect_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Inicia o loop principal do Tkinter
    navegador.mainloop()

# Chamada para iniciar o navegador
iniciar_navegador()
