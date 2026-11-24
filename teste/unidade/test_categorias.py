"""Testes de unidade do módulo Categorias (RF006 a RF009).

Regras cobertas: RN04 (categoria em uso não é excluída), RN09 (categoria
padrão não é alterada nem excluída), RN14 (categoria em uso não muda de
tipo), RN18 (só do próprio usuário), RN21 (nome único por usuário e tipo,
sem diferenciar maiúsculas) e RN22 (categorias padrão criadas no cadastro).

Lembrete das fixtures: o usuário 1 tem 1 "Salário" (receita),
2 "Alimentação" (despesa) e 3 "Lazer" (despesa); o usuário 2 tem
4 "Alimentação" (despesa). O client roda como o usuário 1.
"""
from sqlalchemy import select

from app.models import Categoria, Lancamento
from app.modules.categorias.service import CATEGORIAS_PADRAO


def nova(client, **extra):
    corpo = {"nome": "Educação", "tipo": "despesa"}
    corpo.update(extra)
    return client.post("/categorias", json=corpo)


def com_lancamento(db, categoria_id: int, tipo: str = "despesa") -> None:
    """Coloca a categoria em uso com um lançamento do usuário 1."""
    db.add(
        Lancamento(
            usuario_id=1, categoria_id=categoria_id, tipo=tipo,
            valor="10.00", descricao="Teste",
        )
    )
    db.commit()


def categoria_padrao(db) -> int:
    """Cria uma categoria padrão (RN09) para o usuário 1 e devolve o id."""
    categoria = Categoria(usuario_id=1, nome="Mercado", tipo="despesa", padrao=True)
    db.add(categoria)
    db.commit()
    return categoria.id


# ---------- RF007: consultar ----------
def test_rf007_lista_so_as_categorias_do_usuario(client):
    r = client.get("/categorias")
    assert r.status_code == 200
    ids = [c["id"] for c in r.json()]
    assert sorted(ids) == [1, 2, 3]  # a 4 é do usuário 2


def test_rf007_lista_em_ordem_de_nome(client):
    nomes = [c["nome"] for c in client.get("/categorias").json()]
    assert nomes == ["Alimentação", "Lazer", "Salário"]


def test_rf007_filtro_por_tipo_traz_so_despesas(client):
    r = client.get("/categorias", params={"tipo": "despesa"})
    assert {c["tipo"] for c in r.json()} == {"despesa"}
    assert len(r.json()) == 2


def test_rf007_filtro_com_tipo_invalido_e_recusado(client):
    assert client.get("/categorias", params={"tipo": "outro"}).status_code == 422


def test_rf007_resposta_tem_id_nome_tipo_e_padrao(client):
    item = client.get("/categorias").json()[0]
    assert set(item) == {"id", "nome", "tipo", "padrao"}


# ---------- RF006: cadastrar ----------
def test_rf006_cadastrar_categoria_valida(client):
    r = nova(client)
    assert r.status_code == 201
    assert r.json()["nome"] == "Educação"
    assert r.json()["tipo"] == "despesa"
    assert r.json()["padrao"] is False


def test_rf006_nome_e_salvo_sem_espacos_nas_pontas(client):
    assert nova(client, nome="  Pets  ").json()["nome"] == "Pets"


def test_nome_vazio_ou_so_espacos_e_recusado(client):
    assert nova(client, nome="").status_code == 422
    assert nova(client, nome="   ").status_code == 422


def test_nome_com_mais_de_50_caracteres_e_recusado(client):
    assert nova(client, nome="x" * 51).status_code == 422


def test_tipo_invalido_e_recusado(client):
    assert nova(client, tipo="investimento").status_code == 422


# ---------- RN21: nome único por usuário e tipo ----------
def test_rn21_mesmo_nome_e_tipo_em_minusculas_e_recusado(client):
    r = nova(client, nome="alimentação", tipo="despesa")
    assert r.status_code == 409
    assert r.json()["campo"] == "nome"
    assert r.json()["detail"] == "Você já tem uma categoria com esse nome."


def test_rn21_mesmo_nome_em_outro_tipo_e_aceito(client):
    assert nova(client, nome="Alimentação", tipo="receita").status_code == 201


def test_rn21_nome_igual_ao_de_outro_usuario_e_aceito(client, db):
    # "Viagem" existe só para o usuário 2; o usuário 1 também pode ter a dele
    db.add(Categoria(usuario_id=2, nome="Viagem", tipo="despesa"))
    db.commit()
    assert nova(client, nome="Viagem", tipo="despesa").status_code == 201


# ---------- RF008: alterar ----------
def test_rf008_alterar_nome_de_categoria_propria(client):
    r = client.put("/categorias/3", json={"nome": "Diversão", "tipo": "despesa"})
    assert r.status_code == 200
    assert r.json()["nome"] == "Diversão"


def test_rf008_alterar_mantendo_o_proprio_nome_e_aceito(client):
    # O ignorar_id faz a própria categoria não contar como repetida
    r = client.put("/categorias/3", json={"nome": "LAZER", "tipo": "despesa"})
    assert r.status_code == 200
    assert r.json()["nome"] == "LAZER"


def test_rn21_alterar_para_nome_que_ja_existe_no_tipo_e_recusado(client):
    r = client.put("/categorias/3", json={"nome": "alimentação", "tipo": "despesa"})
    assert r.status_code == 409
    assert r.json()["campo"] == "nome"


# ---------- RN14: categoria em uso não muda de tipo ----------
def test_rn14_categoria_com_lancamento_nao_muda_de_tipo(client, db):
    com_lancamento(db, 3)
    r = client.put("/categorias/3", json={"nome": "Lazer", "tipo": "receita"})
    assert r.status_code == 409
    assert r.json()["campo"] == "tipo"


def test_rn14_categoria_com_lancamento_pode_mudar_so_o_nome(client, db):
    com_lancamento(db, 3)
    r = client.put("/categorias/3", json={"nome": "Diversão", "tipo": "despesa"})
    assert r.status_code == 200


def test_rn14_categoria_sem_uso_pode_mudar_de_tipo(client):
    r = client.put("/categorias/3", json={"nome": "Lazer", "tipo": "receita"})
    assert r.status_code == 200
    assert r.json()["tipo"] == "receita"


# ---------- RN09: categoria padrão ----------
def test_rn09_categoria_padrao_nao_pode_ser_alterada(client, db):
    id_ = categoria_padrao(db)
    r = client.put(f"/categorias/{id_}", json={"nome": "Feira", "tipo": "despesa"})
    assert r.status_code == 403


def test_rn09_categoria_padrao_nao_pode_ser_excluida(client, db):
    id_ = categoria_padrao(db)
    assert client.delete(f"/categorias/{id_}").status_code == 403
    assert db.get(Categoria, id_) is not None


# ---------- RF009: excluir ----------
def test_rf009_excluir_categoria_sem_uso(client):
    r = client.delete("/categorias/3")
    assert r.status_code == 204
    assert r.content == b""
    ids = [c["id"] for c in client.get("/categorias").json()]
    assert 3 not in ids


def test_rn04_categoria_com_lancamento_nao_pode_ser_excluida(client, db):
    com_lancamento(db, 3)
    r = client.delete("/categorias/3")
    assert r.status_code == 409
    assert "não pode ser excluída" in r.json()["detail"]
    assert db.get(Categoria, 3) is not None


# ---------- RN18: só do próprio usuário ----------
def test_rn18_alterar_categoria_de_outro_usuario_responde_404(client):
    r = client.put("/categorias/4", json={"nome": "Comida", "tipo": "despesa"})
    assert r.status_code == 404


def test_rn18_excluir_categoria_de_outro_usuario_responde_404(client, db):
    assert client.delete("/categorias/4").status_code == 404
    assert db.get(Categoria, 4) is not None


def test_alterar_ou_excluir_categoria_inexistente_responde_404(client):
    assert client.put("/categorias/999", json={"nome": "X", "tipo": "despesa"}).status_code == 404
    assert client.delete("/categorias/999").status_code == 404


# ---------- RN22: categorias padrão criadas no cadastro do usuário ----------
def test_rn22_cadastro_de_usuario_cria_as_9_categorias_padrao(client, db):
    corpo = {
        "nome": "Carla",
        "email": "carla@x.com",
        "senha": "senha-forte-123",
        "aceita_politica": True,
    }
    r = client.post("/acesso/cadastro", json=corpo)
    assert r.status_code == 201

    categorias = list(
        db.scalars(select(Categoria).where(Categoria.usuario_id == r.json()["id"]))
    )
    assert len(categorias) == 9 == len(CATEGORIAS_PADRAO)
    assert all(c.padrao for c in categorias)


# ---------- Tabelas de outros módulos que ainda não existem ----------
def _tabela_temporaria(db, nome: str):
    """Simula uma tabela de outra pessoa (conta_pagar, orcamento) com categoria_id."""
    from sqlalchemy import Column, ForeignKey, Integer, Table

    from app.core.database import Base

    tabela = Table(
        nome, Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("categoria_id", Integer, ForeignKey("categoria.id")),
    )
    tabela.create(db.get_bind())
    return tabela


def _remover_tabela(db, tabela) -> None:
    from app.core.database import Base

    db.rollback()
    Base.metadata.remove(tabela)
    tabela.drop(db.get_bind())


def test_rn04_categoria_com_conta_a_pagar_nao_pode_ser_excluida(client, db):
    conta_pagar = _tabela_temporaria(db, "conta_pagar")
    try:
        db.execute(conta_pagar.insert().values(id=1, categoria_id=3))
        db.commit()
        assert client.delete("/categorias/3").status_code == 409
        r = client.put("/categorias/3", json={"nome": "Lazer", "tipo": "receita"})
        assert r.status_code == 409 and r.json()["campo"] == "tipo"  # RN14
    finally:
        _remover_tabela(db, conta_pagar)


def test_rf009_excluir_categoria_apaga_os_limites_de_orcamento(client, db):
    orcamento = _tabela_temporaria(db, "orcamento")
    try:
        db.execute(orcamento.insert().values(id=1, categoria_id=3))
        db.commit()
        assert client.delete("/categorias/3").status_code == 204
        assert db.execute(orcamento.select()).first() is None
    finally:
        _remover_tabela(db, orcamento)


def test_rn21_banco_recusa_duplicada_mesmo_se_a_conferencia_falhar(client, monkeypatch):
    """Simula duas requisições ao mesmo tempo: a conferência do service passa,
    mas o índice único do banco recusa, e a resposta continua sendo 409."""
    from app.modules.categorias import service

    monkeypatch.setattr(service, "_garantir_nome_disponivel", lambda *a, **k: None)
    # Nome sem acento: o lower() do SQLite (banco dos testes) só converte letras ASCII
    r = nova(client, nome="LAZER", tipo="despesa")
    assert r.status_code == 409
    assert r.json()["campo"] == "nome"
