def criar_entregador(client, nome, tipo_veiculo, capacidade_kg):
    resposta = client.post("/entregadores/", json={
        "nome": nome,
        "tipo_veiculo": tipo_veiculo,
        "capacidade_kg": capacidade_kg,
    })
    assert resposta.status_code == 200
    return resposta.json()

def test_criar_entregador_comeca_disponivel(client):
    entregador = criar_entregador(client, "Joao", "moto", 20)
    assert entregador["disponivel"] is True

def test_buscar_entregador_inexistente_retorna_404(client):
    resposta = client.get("/entregadores/9999")
    assert resposta.status_code == 404

def test_atualizar_disponibilidade_parcial(client):
    entregador = criar_entregador(client, "Maria", "carro", 100)
    resposta = client.put(f"/entregadores/{entregador['id']}", json={"disponivel": False})
    assert resposta.status_code == 200
    assert resposta.json()["disponivel"] is False
    assert resposta.json()["nome"] == "Maria"

def test_deletar_entregador(client):
    entregador = criar_entregador(client, "Carlos", "caminhao", 500)
    resposta = client.delete(f"/entregadores/{entregador['id']}")
    assert resposta.status_code == 200
    resposta_get = client.get(f"/entregadores/{entregador['id']}")
    assert resposta_get.status_code == 404