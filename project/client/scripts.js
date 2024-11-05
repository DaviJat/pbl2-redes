const API_URL = 'http://127.0.0.1:5000'; // URL da API

// Função para carregar as rotas com base em origem e destino
async function carregarRotas() {
  const origem = document.getElementById('origem').value;
  const destino = document.getElementById('destino').value;
  const tableBody = document.getElementById('trechosBody');

  // Validação de entrada
  if (!origem || !destino) {
    tableBody.innerHTML = '<tr><td colspan="3">Selecione o destino e a origem para encontrar rotas.</td></tr>';
    return;
  }

  // Mensagem de carregamento enquanto busca dados
  tableBody.innerHTML = '<tr><td colspan="3">Carregando trechos...</td></tr>';
  logStatus("Carregando rotas, por favor aguarde...");

  try {
    const url = new URL(`${API_URL}/trechos`);
    url.searchParams.append("origem", origem);
    url.searchParams.append("destino", destino);

    // Faz a requisição para a API
    const response = await fetch(url);

    if (response.ok) {
      const data = await response.json();

      if (data.length > 0) {
        atualizarTabela(data); // Atualiza a tabela com os dados recebidos
        logStatus("Trechos carregados com sucesso.");
      } else {
        tableBody.innerHTML = '<tr><td colspan="3">Nenhum trecho encontrado.</td></tr>';
        logStatus("Nenhum trecho encontrado.");
      }
    } else {
      tableBody.innerHTML = '<tr><td colspan="3">Erro ao carregar trechos.</td></tr>';
      logStatus("Erro ao carregar trechos.");
    }
  } catch (error) {
    console.error("Erro ao carregar trechos:", error);
    tableBody.innerHTML = '<tr><td colspan="3">Erro ao carregar trechos.</td></tr>';
    logStatus("Erro ao carregar trechos.");
  }
}

// Variável global para armazenar rotas carregadas
let json_rotas = {};

// Função para atualizar a tabela de rotas
function atualizarTabela(rotas) {
  const tableBody = document.getElementById('trechosBody');
  tableBody.innerHTML = ''; // Limpa a tabela antes de preencher com novos dados
  json_rotas = {}; // Limpa o armazenamento anterior de rotas

  rotas.forEach((rota, index) => {
    // Constrói a descrição da rota
    const rotaDescricao = rota.map(trecho => `${trecho.origem} -> ${trecho.destino}`).join(', ');
    const distanciaTotal = rota.reduce((total, trecho) => total + trecho.distancia, 0);

    // Armazena a rota no objeto global json_rotas
    json_rotas[index] = { id: index, rota: rota };

    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${rotaDescricao}</td>
      <td>${distanciaTotal}</td>
      <td><button onclick="confirmarCompra(event, ${index})">Comprar</button></td>
    `;
    tableBody.appendChild(row);
  });
}

// Função para confirmar a compra de uma rota
async function confirmarCompra(event, id) {
  event.preventDefault(); // Impede o comportamento padrão do botão dentro de um formulário
  const rota = json_rotas[id].rota;
  const rotaDescricao = rota.map(trecho => `${trecho.origem} -> ${trecho.destino}`).join(', ');

  logStatus("Processando a compra, por favor aguarde...");

  try {
    const response = await fetch(`${API_URL}/comprar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rota })
    });

    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === "success") {
      logStatus(`Compra realizada com sucesso para a rota: ${rotaDescricao}`);
      limparTabela();
    } else {
      logStatus(`Erro ao realizar a compra para a rota: ${rotaDescricao}`);
    }
  } catch (error) {
    console.error("Erro ao confirmar compra:", error);
    logStatus(`Erro ao confirmar compra para a rota: ${rotaDescricao}. Tente novamente mais tarde.`);
  }
}

// Função para limpar a tabela de rotas sem limpar o log ou resetar o formulário
function limparTabela() {
  const tableBody = document.getElementById('trechosBody');
  tableBody.innerHTML = '<tr><td colspan="3">Selecione o destino e a origem para encontrar rotas.</td></tr>';
}

// Função para exibir logs no painel de status
function logStatus(message) {
  const logElement = document.getElementById('log');
  const timestamp = new Date().toLocaleTimeString();
  logElement.innerHTML += `<p>[${timestamp}] ${message}</p>`;
}
