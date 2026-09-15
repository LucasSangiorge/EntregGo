def criar_produto(client, **kwargs):
    dados = {
        "nome": "Caixa Eletronicos",
        "peso_kg": 5.5,
        "altura_cm": 30,
        "largura_cm": 20,
        "profundidade_cm": 15,
        "cidade_origem": "Belo Horizonte",
        "cidade_destino": "Contagem",
    }
    dados.update(kwargs)
    resposta = client.post("/produtos/", json=dados)
    assert resposta.status_code == 200
    return resposta.json()

def test_criar_produto_com_dados_corretos(client):
    produto = criar_produto(client, nome="Notebook", peso_kg=2.3)
    assert produto["nome"] == "Notebook"
    assert produto["peso_kg"] == 2.3

def test_buscar_produto_inexistente_retorna_404(client):
    resposta = client.get("/produtos/9999")
    assert resposta.status_code == 404

def test_atualizar_peso_parcial(client):
    produto = criar_produto(client)
    resposta = client.put(f"/produtos/{produto['id']}", json={"peso_kg": 10.0})
    assert resposta.status_code == 200
    assert resposta.json()["peso_kg"] == 10.0
    assert resposta.json()["cidade_origem"] == "Belo Horizonte"

def test_deletar_produto(client):
    produto = criar_produto(client)
    resposta = client.delete(f"/produtos/{produto['id']}")
    assert resposta.status_code == 200
    resposta_get = client.get(f"/produtos/{produto['id']}")
    assert resposta_get.status_code == 404