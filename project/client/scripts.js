const API_URL = 'http://127.0.0.1:5000';

async function carregarRotas() {
  const origem = document.getElementById('origem').value;
  const destino = document.getElementById('destino').value;

  const tableBody = document.getElementById('trechosBody');

  if (!origem || !destino) {
      tableBody.innerHTML = '<tr><td colspan="3">Selecione o destino e a origem para encontrar rotas.</td></tr>';
      return;
  }

  tableBody.innerHTML = '<tr><td colspan="3">Carregando trechos...</td></tr>';

  try {
      const url = new URL(`${API_URL}/trechos`);
      url.searchParams.append("origem", origem);
      url.searchParams.append("destino", destino);

      const response = await fetch(url);
      if (response.ok) {
          const data = await response.json();
          console.log(data)
          if (data.length > 0) {
              atualizarTabela(data);
              logStatus("Trechos carregados com sucesso.");
          } else {
              tableBody.innerHTML = '<tr><td colspan="3">Nenhum trecho encontrado.</td></tr>';
              logStatus("Nenhum trecho encontrado.");
          }
      } else {
          logStatus("Erro ao carregar trechos.");
          tableBody.innerHTML = '<tr><td colspan="3">Erro ao carregar trechos.</td></tr>';
      }
  } catch (error) {
      console.error("Erro ao carregar trechos:", error);
      logStatus("Erro ao carregar trechos.");
      tableBody.innerHTML = '<tr><td colspan="3">Erro ao carregar trechos.</td></tr>';
  }
}

// Declaração global de json_rotas
let json_rotas = {};

function atualizarTabela(rotas) {
  const tableBody = document.getElementById('trechosBody');
  tableBody.innerHTML = '';

  // Redefine o objeto json_rotas para evitar acúmulo de dados antigos
  json_rotas = {};

  if (rotas.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="3">Nenhum trecho encontrado.</td></tr>';
    return;
  }

  rotas.forEach((rota, index) => {
    // Array para armazenar a descrição da rota (origem -> destino)
    const rotaDescricao = rota.map(trecho => `${trecho.origem} -> ${trecho.destino}`).join(', ');

    // Soma as distâncias da rota
    const distanciaTotal = rota.reduce((total, trecho) => total + trecho.distancia, 0);

    // Adiciona ao objeto json_rotas global
    json_rotas[index] = {
      id: index,
      rota: rota
    };

    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${rotaDescricao}</td>
      <td>${distanciaTotal}</td>
      <td><button onclick="confirmarCompra(${index})">Comprar</button></td>
    `;
    tableBody.appendChild(row);
  });
}

async function confirmarCompra(id) {
  // Obtém a rota específica a partir de json_rotas
  const rota = json_rotas[id].rota;
  
  try {
    const response = await fetch(`${API_URL}/comprar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rota })  // Envia a rota específica no formato correto
    });

    const data = await response.json();

    if (response.ok) {
      logStatus(`Compra confirmada para a rota: ${data.status}`);
      carregarRotas();
    } else {
      logStatus(`Erro ao confirmar compra para a rota: ${data.error}`);
    }
  } catch (error) {
    console.error("Erro ao confirmar compra:", error);
    logStatus("Erro ao confirmar compra.");
  }
}


function logStatus(message) {
  const logElement = document.getElementById('log');
  const timestamp = new Date().toLocaleTimeString();
  logElement.innerHTML += `<p>[${timestamp}] ${message}</p>`;
}
