from app.crud.entrega import calcular_tipo_veiculo

def criar_produto(client, **kwargs):
    dados = {
        "nome": "Caixa",
        "peso_kg": 5.0,
        "altura_cm": 30,
        "largura_cm": 20,
        "profundidade_cm": 15,
        "cidade_origem": "Belo Horizonte",
        "cidade_destino": "Contagem",
    }
    dados.update(kwargs)
    resposta = client.post("/produtos/", json=dados)
    return resposta.json()

def criar_entregador(client, **kwargs):
    dados = {"nome": "Joao", "tipo_veiculo": "moto", "capacidade_kg": 20}
    dados.update(kwargs)
    resposta = client.post("/entregadores/", json=dados)
    return resposta.json()

def test_criar_entrega_nasce_pendente_sem_entregador(client):
    produto = criar_produto(client)
    resposta = client.post("/entregas/", json={"produto_id": produto["id"]})
    entrega = resposta.json()

    assert resposta.status_code == 200
    assert entrega["status"] == "pendente"
    assert entrega["entregador_id"] is None

def test_criar_entrega_com_produto_inexistente_retorna_404(client):
    resposta = client.post("/entregas/", json={"produto_id": 9999})
    assert resposta.status_code == 404

def test_criar_entrega_com_entregador_inexistente_retorna_404(client):
    produto = criar_produto(client)
    resposta = client.post("/entregas/", json={"produto_id": produto["id"], "entregador_id": 9999})
    assert resposta.status_code == 404

def test_atualizar_status_da_entrega(client):
    produto = criar_produto(client)
    entrega = client.post("/entregas/", json={"produto_id": produto["id"]}).json()

    resposta = client.put(f"/entregas/{entrega['id']}", json={"status": "em_transporte"})
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "em_transporte"

def test_calcula_moto_para_produto_leve_e_pequeno():
    assert calcular_tipo_veiculo(peso_kg=5, maior_dimensao_cm=30) == "moto"

def test_calcula_caminhao_para_produto_leve_mas_comprido():
    assert calcular_tipo_veiculo(peso_kg=4, maior_dimensao_cm=200) == "caminhao"

def test_calcula_caminhao_para_produto_pesado_mas_pequeno():
    assert calcular_tipo_veiculo(peso_kg=80, maior_dimensao_cm=30) == "caminhao"

def test_atribuir_entregador_com_sucesso(client):
    criar_entregador(client, tipo_veiculo="carro")
    produto = criar_produto(client, peso_kg=20)
    entrega = client.post("/entregas/", json={"produto_id": produto["id"]}).json()

    resposta = client.post(f"/entregas/{entrega['id']}/atribuir")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "em_transporte"
    assert resposta.json()["entregador_id"] is not None

def test_atribuir_sem_entregador_disponivel_retorna_409(client):
    produto = criar_produto(client, peso_kg=20)
    entrega = client.post("/entregas/", json={"produto_id": produto["id"]}).json()

    resposta = client.post(f"/entregas/{entrega['id']}/atribuir")
    assert resposta.status_code == 409
