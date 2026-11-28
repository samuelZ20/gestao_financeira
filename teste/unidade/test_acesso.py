"""Testes de unidade do módulo de acesso (cadastro e login).

Regras cobertas:
- RN01: o e-mail é único, sem diferenciar maiúsculas e minúsculas.
- RN15: sem aceitar a política de privacidade, não há cadastro.
- RN16: senha com pelo menos 8 caracteres, guardada só como hash.
- RF002: login com a mesma mensagem para e-mail ou senha errados.

O conftest já cria a usuária Ana (ana@x.com).
"""
from sqlalchemy import select

from app.models import Usuario


def dados_cadastro(**extra):
    """Dados válidos de cadastro; o teste troca só o campo que quer testar."""
    dados = {"nome": "Carla", "email": "carla@x.com", "senha": "12345678", "aceita_politica": True}
    dados.update(extra)
    return dados


def test_rf001_cadastro_valido_cria_o_usuario(client, db):
    resposta = client.post("/acesso/cadastro", json=dados_cadastro())

    assert resposta.status_code == 201
    assert resposta.json()["email"] == "carla@x.com"
    assert db.scalar(select(Usuario).where(Usuario.email == "carla@x.com")) is not None


def test_rn01_email_ja_cadastrado_e_recusado(client):
    resposta = client.post("/acesso/cadastro", json=dados_cadastro(email="ana@x.com"))

    assert resposta.status_code == 409
    assert resposta.json()["detail"] == "Este e-mail já está cadastrado."


def test_rn01_email_com_maiusculas_conta_como_o_mesmo(client):
    resposta = client.post("/acesso/cadastro", json=dados_cadastro(email="ANA@X.COM"))

    assert resposta.status_code == 409


def test_rn01_email_e_salvo_em_minusculas(client):
    resposta = client.post("/acesso/cadastro", json=dados_cadastro(email="Carla@X.com"))

    assert resposta.json()["email"] == "carla@x.com"


def test_rn15_cadastro_sem_aceitar_a_politica_e_recusado(client):
    resposta = client.post("/acesso/cadastro", json=dados_cadastro(aceita_politica=False))

    assert resposta.status_code == 422


def test_rn16_senha_com_menos_de_8_caracteres_e_recusada(client):
    resposta = client.post("/acesso/cadastro", json=dados_cadastro(senha="1234567"))

    assert resposta.status_code == 422


def test_rn16_senha_e_guardada_so_como_hash(client, db):
    client.post("/acesso/cadastro", json=dados_cadastro())

    usuario = db.scalar(select(Usuario).where(Usuario.email == "carla@x.com"))
    assert usuario.senha_hash != "12345678"
    assert usuario.senha_hash.startswith("$2b$")


def test_rf002_login_valido_devolve_o_token(client):
    client.post("/acesso/cadastro", json=dados_cadastro())

    resposta = client.post("/acesso/login", json={"email": "carla@x.com", "senha": "12345678"})

    assert resposta.status_code == 200
    assert resposta.json()["token_type"] == "bearer"
    assert resposta.json()["access_token"]


def test_rf002_senha_errada_e_email_inexistente_tem_a_mesma_mensagem(client):
    client.post("/acesso/cadastro", json=dados_cadastro())

    senha_errada = client.post("/acesso/login", json={"email": "carla@x.com", "senha": "senhaerrada"})
    email_inexistente = client.post("/acesso/login", json={"email": "ninguem@x.com", "senha": "12345678"})

    assert senha_errada.status_code == 401
    assert email_inexistente.status_code == 401
    assert senha_errada.json()["detail"] == email_inexistente.json()["detail"]