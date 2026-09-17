const API_URL = "";

const tabelaPainel = new Tabulator("#tabela-painel", {
    layout: "fitColumns",
    placeholder: "Nenhuma entrega registrada ainda",
    columns: [
        { title: "Entrega #", field: "id", width: 90 },
        { title: "Produto", field: "produto_nome" },
        { title: "Origem → Destino", field: "rota" },
        { title: "Peso (kg)", field: "peso_kg", width: 100 },
        { title: "Entregador", field: "entregador_nome" },
        { title: "Veículo", field: "tipo_veiculo" },
        {
            title: "Status",
            field: "status",
            formatter: (cell) => {
                const status = cell.getValue();
                return `<span class="badge ${status}">${status.replace("_", " ")}</span>`;
            },
        },
    ],
});

function renderStats(entregas) {
    const total = entregas.length;
    const pendentes = entregas.filter((e) => e.status === "pendente").length;
    const emTransporte = entregas.filter((e) => e.status === "em_transporte").length;
    const entregues = entregas.filter((e) => e.status === "entregue").length;

    document.getElementById("stats").innerHTML = `
        <div class="stat"><div class="numero">${total}</div><div class="rotulo">Total de entregas</div></div>
        <div class="stat"><div class="numero">${pendentes}</div><div class="rotulo">Pendentes</div></div>
        <div class="stat"><div class="numero">${emTransporte}</div><div class="rotulo">Em transporte</div></div>
        <div class="stat"><div class="numero">${entregues}</div><div class="rotulo">Entregues</div></div>
    `;
}

async function carregarPainel() {
    const [entregasResp, produtosResp, entregadoresResp] = await Promise.all([
        fetch(`${API_URL}/entregas/`),
        fetch(`${API_URL}/produtos/`),
        fetch(`${API_URL}/entregadores/`),
    ]);

    const entregas = await entregasResp.json();
    const produtos = await produtosResp.json();
    const entregadores = await entregadoresResp.json();

    const produtoPorId = Object.fromEntries(produtos.map((p) => [p.id, p]));
    const entregadorPorId = Object.fromEntries(entregadores.map((e) => [e.id, e]));

    const linhas = entregas.map((entrega) => {
        const produto = produtoPorId[entrega.produto_id];
        const entregador = entregadorPorId[entrega.entregador_id];
        return {
            id: entrega.id,
            status: entrega.status,
            produto_nome: produto ? produto.nome : "—",
            peso_kg: produto ? produto.peso_kg : "—",
            rota: produto ? `${produto.cidade_origem} → ${produto.cidade_destino}` : "—",
            entregador_nome: entregador ? entregador.nome : "Aguardando",
            tipo_veiculo: entregador ? entregador.tipo_veiculo : "—",
        };
    });

    tabelaPainel.setData(linhas);
    renderStats(entregas);
}

document.getElementById("btn-atualizar-painel").addEventListener("click", carregarPainel);

carregarPainel();
