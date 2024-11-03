const API_URL = 'http://127.0.0.1:5000';

async function carregarRotas() {
  const origem = document.getElementById('origem').value;
  const destino = document.getElementById('destino').value;
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

  if (trechos.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="3">Nenhum trecho encontrado.</td></tr>';
    return;
  }

  console.log(trechos);

  trechos.forEach((trecho, index) => {
    console.log(trecho);
    const rota = trecho.rota || trecho.caminho; // Usa 'rota' se existir, senão usa 'caminho'
    
    // Verifica se 'rota' ou 'caminho' é um array
    if (Array.isArray(rota)) {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${rota.join(' -> ')}</td>
        <td>${trecho.distancia}</td>
        <td><button onclick="iniciarReserva(${index})">Reservar</button></td>
      `;
      tableBody.appendChild(row);
    } else {
      console.warn(`Formato inesperado para trecho ${index}: `, trecho);
    }
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
