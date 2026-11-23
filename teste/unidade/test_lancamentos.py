"""Testes de unidade do módulo Lançamentos (RF010 a RF013).

Regras cobertas: RN02 (valor > 0 e categoria do mesmo tipo), RN03 (saldo
calculado), RN10 (lançamento de conta paga) e RN18 (só do próprio usuário).
"""
from datetime import date

from app.core.database import Base
from app.models import Lancamento


def novo(client, **extra):
    corpo = {
        "tipo": "despesa",
        "descricao": "Almoço",
        "valor": "120.00",
        "data": "2026-11-10",
        "categoria_id": 2,
    }
    corpo.update(extra)
    return client.post("/lancamentos", json=corpo)


# ---------- RF010: registrar ----------
def test_registrar_despesa_valida(client):
    r = novo(client)
    assert r.status_code == 201
    assert r.json()["descricao"] == "Almoço"
    assert r.json()["categoria"]["nome"] == "Alimentação"


def test_registrar_usa_data_de_hoje_por_padrao(client):
    corpo = {"tipo": "despesa", "descricao": "Café", "valor": "5", "categoria_id": 2}
    r = client.post("/lancamentos", json=corpo)
    assert r.json()["data"] == date.today().isoformat()


def test_rn02_valor_zero_ou_negativo_e_recusado(client):
    assert novo(client, valor="0").status_code == 422
    assert novo(client, valor="-10").status_code == 422


def test_rn02_categoria_de_outro_tipo_e_recusada(client):
    r = novo(client, tipo="despesa", categoria_id=1)  # 1 é de receita
    assert r.status_code == 422
    assert r.json()["campo"] == "categoria_id"


def test_rn23_descricao_em_branco_e_recusada(client):
    assert novo(client, descricao="   ").status_code == 422


def test_categoria_de_outro_usuario_nao_existe_para_mim(client):
    assert novo(client, categoria_id=4).status_code == 422


# ---------- RF011: consultar o mês e saldo (RN03) ----------
def test_rn03_saldo_do_periodo_e_receitas_menos_despesas(client):
    novo(client, tipo="receita", valor="500.00", categoria_id=1, descricao="Salário")
    novo(client, valor="120.00")  # critério de aceitação: 500 - 120 = 380
    r = client.get("/lancamentos", params={"ano": 2026, "mes": 11})
    assert r.json()["quantidade"] == 2
    assert r.json()["saldo_periodo"] == "380.00"


def test_consulta_so_traz_o_mes_pedido_do_mais_novo_para_o_mais_antigo(client):
    novo(client, data="2026-11-02", descricao="A")
    novo(client, data="2026-11-20", descricao="B")
    novo(client, data="2026-10-30", descricao="Fora")
    itens = client.get("/lancamentos", params={"ano": 2026, "mes": 11}).json()["itens"]
    assert [i["descricao"] for i in itens] == ["B", "A"]


def test_filtros_por_tipo_e_por_categoria(client):
    novo(client, tipo="receita", categoria_id=1, descricao="Salário", valor="1000")
    novo(client, categoria_id=2, descricao="Mercado")
    novo(client, categoria_id=3, descricao="Cinema")
    base = {"ano": 2026, "mes": 11}
    so_saidas = client.get("/lancamentos", params={**base, "tipo": "despesa"}).json()
    assert so_saidas["quantidade"] == 2
    so_lazer = client.get("/lancamentos", params={**base, "categoria_id": 3}).json()
    assert [i["descricao"] for i in so_lazer["itens"]] == ["Cinema"]


def test_mes_sem_lancamentos_volta_lista_vazia(client):
    r = client.get("/lancamentos", params={"ano": 2020, "mes": 1}).json()
    assert r["itens"] == [] and r["saldo_periodo"] == "0"


# ---------- RN18: isolamento entre usuários ----------
def test_rn18_nao_lista_nem_altera_nem_exclui_de_outro_usuario(client, db):
    db.add(Lancamento(usuario_id=2, categoria_id=4, tipo="despesa", valor=10,
                      data=date(2026, 11, 5), descricao="Do Beto"))
    db.commit()
    id_do_beto = db.query(Lancamento).one().id

    assert client.get("/lancamentos", params={"ano": 2026, "mes": 11}).json()["quantidade"] == 0
    corpo = {"tipo": "despesa", "descricao": "x", "valor": "1", "categoria_id": 2}
    assert client.put(f"/lancamentos/{id_do_beto}", json=corpo).status_code == 404
    assert client.delete(f"/lancamentos/{id_do_beto}").status_code == 404


# ---------- RF012: alterar ----------
def test_alterar_lancamento(client):
    id_ = novo(client).json()["id"]
    r = client.put(f"/lancamentos/{id_}", json={
        "tipo": "despesa", "descricao": "Jantar", "valor": "80.50",
        "data": "2026-11-11", "categoria_id": 3})
    assert r.status_code == 200
    assert r.json()["descricao"] == "Jantar"
    assert r.json()["categoria"]["id"] == 3


def test_alterar_com_categoria_de_outro_tipo_e_recusado(client):
    id_ = novo(client).json()["id"]
    r = client.put(f"/lancamentos/{id_}", json={
        "tipo": "despesa", "descricao": "x", "valor": "1", "categoria_id": 1})
    assert r.status_code == 422


# ---------- RF013: excluir ----------
def test_excluir_lancamento(client):
    id_ = novo(client).json()["id"]
    assert client.delete(f"/lancamentos/{id_}").status_code == 204
    assert client.get("/lancamentos", params={"ano": 2026, "mes": 11}).json()["quantidade"] == 0


def test_excluir_inexistente_da_404(client):
    assert client.delete("/lancamentos/999").status_code == 404


# ---------- RN10: lançamento gerado por conta paga ----------
def test_rn10_lancamento_de_conta_paga_nao_pode_ser_alterado_nem_excluido(client, db):
    """Simula a tabela conta_pagar (da pessoa C) apontando para o lançamento."""
    from sqlalchemy import Column, ForeignKey, Integer, Table

    conta_pagar = Table(
        "conta_pagar", Base.metadata,
        Column("id", Integer, primary_key=True),
        Column("lancamento_id", Integer, ForeignKey("lancamento.id")),
    )
    conta_pagar.create(db.get_bind())
    try:
        id_ = novo(client).json()["id"]
        db.execute(conta_pagar.insert().values(id=1, lancamento_id=id_))
        db.commit()

        corpo = {"tipo": "despesa", "descricao": "x", "valor": "1", "categoria_id": 2}
        r1 = client.put(f"/lancamentos/{id_}", json=corpo)
        r2 = client.delete(f"/lancamentos/{id_}")
        assert r1.status_code == 409 and r2.status_code == 409
        assert "conta a pagar" in r1.json()["detail"]
        item = client.get("/lancamentos", params={"ano": 2026, "mes": 11}).json()["itens"][0]
        assert item["gerado_por_conta"] is True
    finally:
        db.rollback()
        Base.metadata.remove(conta_pagar)
        conta_pagar.drop(db.get_bind())
