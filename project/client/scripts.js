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

function atualizarTabela(trechos) {
  const tableBody = document.getElementById('trechosBody');
  tableBody.innerHTML = '';

  if (trechos.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="3">Nenhum trecho encontrado.</td></tr>';
    return;
  }
  console.log(trechos)

  trechos.forEach((trecho) => {
    const rota = trecho.rota || trecho.caminho;

    if (Array.isArray(rota)) {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${rota.join(' -> ')}</td>
        <td>${trecho.distancia}</td>
        <td><button onclick="confirmarCompra(${trecho})">Comprar</button></td>
      `;
      tableBody.appendChild(row);
    } else {
      console.warn("Formato inesperado para trecho: ", trecho);
    }
  });
}

async function confirmarCompra(trechos) {
  try {
    console.log("Confirmando compra para a rota:", rotas);  // Exibir os trechos da rota no console

    const response = await fetch(`${API_URL}/confirm_purchase`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rotas })  // Enviar a lista de rotas completa
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
