const API_URL = "";

function showMessage(elementId, text, isError) {
    const el = document.getElementById(elementId);
    el.textContent = text;
    el.className = "msg " + (isError ? "erro" : "sucesso");
}

const tabelaEntregadores = new Tabulator("#tabela-entregadores", {
    layout: "fitColumns",
    placeholder: "Nenhum entregador cadastrado ainda",
    columns: [
        { title: "ID", field: "id", width: 60 },
        { title: "Nome", field: "nome" },
        { title: "Veículo", field: "tipo_veiculo" },
        { title: "Capacidade (kg)", field: "capacidade_kg" },
        {
            title: "Status",
            field: "disponivel",
            formatter: (cell) => {
                const disponivel = cell.getValue();
                return `<span class="badge ${disponivel ? "disponivel" : "ocupado"}">${disponivel ? "Disponível" : "Ocupado"}</span>`;
            },
        },
    ],
});

async function carregarEntregadores() {
    const resposta = await fetch(`${API_URL}/entregadores/`);
    const entregadores = await resposta.json();
    tabelaEntregadores.setData(entregadores);
}

document.getElementById("btn-atualizar").addEventListener("click", carregarEntregadores);

document.getElementById("form-entregador").addEventListener("submit", async (event) => {
    event.preventDefault();
    const nome = document.getElementById("nome").value;
    const tipo_veiculo = document.getElementById("tipo_veiculo").value;
    const capacidade_kg = Number(document.getElementById("capacidade_kg").value);

    const resposta = await fetch(`${API_URL}/entregadores/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome, tipo_veiculo, capacidade_kg }),
    });

    if (resposta.ok) {
        showMessage("msg-entregador", "Entregador contratado com sucesso!", false);
        event.target.reset();
        carregarEntregadores();
    } else {
        const erro = await resposta.json();
        showMessage("msg-entregador", erro.detail || "Erro ao contratar entregador", true);
    }
});

carregarEntregadores();
