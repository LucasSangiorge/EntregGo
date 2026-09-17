const API_URL = "";

function showMessage(elementId, text, isError) {
    const el = document.getElementById(elementId);
    el.textContent = text;
    el.className = "msg " + (isError ? "erro" : "sucesso");
}

async function atribuirEntregador(entregaId) {
    const resposta = await fetch(`${API_URL}/entregas/${entregaId}/atribuir`, { method: "POST" });
    if (resposta.ok) {
        showMessage("msg-entrega", `Entrega #${entregaId}: entregador atribuído!`, false);
    } else {
        const erro = await resposta.json();
        showMessage("msg-entrega", `Entrega #${entregaId}: ${erro.detail}`, true);
    }
    carregarEntregas();
}

const tabelaEntregas = new Tabulator("#tabela-entregas", {
    layout: "fitColumns",
    placeholder: "Nenhuma encomenda cadastrada ainda",
    columns: [
        { title: "ID", field: "id", width: 60 },
        { title: "Produto ID", field: "produto_id", width: 100 },
        { title: "Entregador ID", field: "entregador_id", width: 120 },
        {
            title: "Status",
            field: "status",
            formatter: (cell) => {
                const status = cell.getValue();
                return `<span class="badge ${status}">${status.replace("_", " ")}</span>`;
            },
        },
        {
            title: "Ação",
            formatter: () => `<button class="secundario">Atribuir entregador</button>`,
            width: 190,
            cellClick: (e, cell) => atribuirEntregador(cell.getRow().getData().id),
        },
    ],
});

async function carregarEntregas() {
    const resposta = await fetch(`${API_URL}/entregas/`);
    const entregas = await resposta.json();
    tabelaEntregas.setData(entregas);
}

document.getElementById("btn-atualizar-entregas").addEventListener("click", carregarEntregas);

async function carregarProdutosNoSelect() {
    const resposta = await fetch(`${API_URL}/produtos/`);
    const produtos = await resposta.json();
    const select = document.getElementById("e-produto-id");
    select.innerHTML = produtos
        .map((p) => `<option value="${p.id}">#${p.id} — ${p.nome} (${p.peso_kg}kg)</option>`)
        .join("");
}

document.getElementById("form-produto").addEventListener("submit", async (event) => {
    event.preventDefault();
    const dados = {
        nome: document.getElementById("p-nome").value,
        peso_kg: Number(document.getElementById("p-peso").value),
        altura_cm: Number(document.getElementById("p-altura").value),
        largura_cm: Number(document.getElementById("p-largura").value),
        profundidade_cm: Number(document.getElementById("p-profundidade").value),
        cidade_origem: document.getElementById("p-origem").value,
        cidade_destino: document.getElementById("p-destino").value,
    };

    const resposta = await fetch(`${API_URL}/produtos/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    });

    if (resposta.ok) {
        showMessage("msg-produto", "Produto cadastrado com sucesso!", false);
        event.target.reset();
        carregarProdutosNoSelect();
    } else {
        const erro = await resposta.json();
        showMessage("msg-produto", erro.detail || "Erro ao cadastrar produto", true);
    }
});

document.getElementById("form-entrega").addEventListener("submit", async (event) => {
    event.preventDefault();
    const produto_id = Number(document.getElementById("e-produto-id").value);

    const resposta = await fetch(`${API_URL}/entregas/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ produto_id }),
    });

    if (resposta.ok) {
        showMessage("msg-entrega", "Entrega criada como pendente!", false);
        carregarEntregas();
    } else {
        const erro = await resposta.json();
        showMessage("msg-entrega", erro.detail || "Erro ao criar entrega", true);
    }
});

carregarProdutosNoSelect();
carregarEntregas();
