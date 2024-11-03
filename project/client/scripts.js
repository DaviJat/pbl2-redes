const API_URL = 'http://127.0.0.1:5000';

async function carregarTrechos(origem = '', destino = '') {
  try {
    const url = new URL(`${API_URL}/trechos`);
    if (origem) url.searchParams.append("origem", origem);
    if (destino) url.searchParams.append("destino", destino);

    const response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      atualizarTabela(data);
      logStatus("Trechos carregados com sucesso.");
    } else {
      logStatus("Erro ao carregar trechos.");
    }
  } catch (error) {
    console.error("Erro ao carregar trechos:", error);
    logStatus("Erro ao carregar trechos.");
  }
}

function atualizarTabela(trechos) {
  const tableBody = document.getElementById('trechosBody');
  tableBody.innerHTML = '';
  trechos.forEach(trecho => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${trecho.id}</td>
      <td>${trecho.rota.split(" -> ")[0]}</td>
      <td>${trecho.rota.split(" -> ")[1]}</td>
      <td><button onclick="iniciarReserva('${trecho.id}')">Reservar</button></td>
    `;
    tableBody.appendChild(row);
  });
}

async function iniciarReserva(trechoId) {
  console.log(`Solicitar reserva para o trecho: ${trechoId}`);
  logStatus(`Reserva solicitada para o trecho ${trechoId}.`);
}

function logStatus(message) {
  const logElement = document.getElementById('log');
  const timestamp = new Date().toLocaleTimeString();
  logElement.innerHTML += `<p>[${timestamp}] ${message}</p>`;
}

async function confirmarCompra() {
  const trechoId = document.getElementById('trechoIdCompra').value;

  try {
    const response = await fetch(`${API_URL}/confirm_purchase`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ trecho_id: trechoId })
    });
    const data = await response.json();
    if (response.ok) {
      logStatus(`Compra confirmada para o trecho ${trechoId}: ${data.status}`);
      carregarTrechos();
    } else {
      logStatus(`Erro ao confirmar compra para o trecho ${trechoId}: ${data.error}`);
    }
  } catch (error) {
    console.error("Erro ao confirmar compra:", error);
    logStatus("Erro ao confirmar compra.");
  }
}
