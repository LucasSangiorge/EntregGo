# EntregGo

Terceiro projeto de estudo do Lucas, depois do [ShopFlowAPI](../ShopFlowAPI) e do [DigitalBankAPI](../DigitalBankAPI). Domínio: plataforma de logística/entregas, no espírito do que Shopee/Mercado Livre fazem (cadastro de produto com origem/destino, atribuição de entregador conforme peso/tamanho).

## Contexto

Lucas é estudante de ADS (Estácio, formatura ~dezembro/2026), migrando de carreira da Logística (trabalhou na CUE - Hospitais e Clínicas) pra Desenvolvimento Backend — esse domínio (logística) é área que ele já conhece na prática, diferencial real de portfólio.

**Objetivo específico deste projeto**: já pratica lógica de programação em Python todo dia, sozinho — o que falta é prática específica com **FastAPI** (rotas, dependency injection, Pydantic, integração com banco) e reforço de **PostgreSQL**. Não é sobre aprender lógica nova, é sobre fluência na ferramenta.

Mesmo método de trabalho do DigitalBankAPI: Lucas digita o código, a IA revisa linha a linha e explica o porquê de cada erro — não escrever código de produção por ele. Código mostrado no chat (não editado direto no arquivo dele), pra ele copiar/digitar.

## Domínio: logística de entregas

Cadastro de entregadores (funcionário do galpão cadastra), cadastro de produtos (origem, destino, peso, dimensões), e atribuição do entregador/veículo adequado pra cada entrega.

## Entidades planejadas (v1 — sem IA ainda)

**`Entregador`**:
- `id`, `nome: str`, `tipo_veiculo: str` (`"moto"`/`"carro"`/`"caminhao"`), `capacidade_kg: float`, `disponivel: bool` (default `True`)

**`Produto`**:
- `id`, `nome: str`, `peso_kg: float`, `altura_cm: float`, `largura_cm: float`, `profundidade_cm: float`, `cidade_origem: str`, `cidade_destino: str`

**`Entrega`**:
- `id`, `produto_id` (FK), `entregador_id` (FK, nullable até ser atribuído), `status: str` (`"pendente"`/`"em_transporte"`/`"entregue"`), `created_at: datetime`
- Regra de negócio central: baseado no peso/dimensão do `Produto`, o sistema decide automaticamente que tipo de veículo é necessário, e atribui um `Entregador` disponível daquele tipo — mesmo padrão de "regra de negócio automática" que o `Transfer` tinha no DigitalBankAPI, aplicado a logística em vez de dinheiro.

## Evolução futura (fora do escopo inicial)

- IA pra otimizar escolha de entregador (proximidade, roteirização) — só depois da regra simples funcionar.
- Dashboard visual bonito — depois do backend/frontend básico funcionando.
- Banco não-relacional (MongoDB) foi cogitado pra dado de rastreamento, mas descartado por ora — v1 é 100% PostgreSQL, foco em fluência com FastAPI, não em introduzir banco novo ainda.

## Decisões técnicas

- **Stack**: FastAPI + SQLAlchemy + PostgreSQL (via Neon, mesmo padrão do DigitalBankAPI) + Pydantic.
- **Deploy**: mesma esteira do DigitalBankAPI — GitHub Actions (CI, testes) + Render (CD, deploy automático a cada push).
- Reaproveitar convenções já fixadas: 4 espaços de indentação, singular/plural em nomes de função, update sempre parcial, `__tablename__` em inglês plural, 404 tratado em toda busca por id, arquitetura em camadas (model → schema → crud → router).

## Status

Banco no Neon criado, `database.py` configurado, repositório no GitHub conectado (`github.com/LucasSangiorge/EntregGo`), CI configurado (`.github/workflows/tests.yml`, GitHub Actions rodando testes a cada push).

As três entidades (`Entregador`, `Produto`, `Entrega`) têm CRUD completo (model → schema → crud → router, registradas no `main.py`), com testes automatizados via pytest (SQLite em memória, isolado do Neon) — 12 testes passando. `Entrega` já valida a existência de `produto_id`/`entregador_id` antes do insert (retorna 404 em vez de deixar a violação de FK do Postgres estourar como 500).

**Falta**: a regra de negócio central (atribuição automática de entregador por peso/tipo de veículo) ainda não foi implementada — só existe o CRUD genérico de `Entrega`. Decisão tomada: a atribuição vai ser uma ação separada da criação (ex.: `POST /entregas/{id}/atribuir`), não automática no `POST /entregas/`, pra imitar melhor o fluxo real (pedido existe primeiro, atribuição acontece depois) e facilitar teste isolado de cada etapa.

Sem Alembic neste projeto (decisão consciente, ver seção de Decisões técnicas — o próximo projeto de portfólio depois deste é que vai introduzir Alembic desde o início).a
