# Meu Bolso

Aplicação web de finanças pessoais para uma pessoa controlar receitas, despesas, contas a pagar, orçamento por categoria e metas de compra.

**Disciplina:** GCC 188 – Engenharia de Software – Universidade Federal de Lavras (UFLA)

**Equipe:**

- Samuel Frizzone Cardoso
- Gabriel Duarte Paiva
- Victor Hugo Faria Aleixo
## Sumário

1. [Contexto do problema e solução](#1-contexto-do-problema-e-solução)
2. [Instruções para uso](#2-instruções-para-uso)
3. [Instruções para devs](#3-instruções-para-devs)
4. [Tecnologias](#4-tecnologias)
5. [Organização do projeto](#5-organização-do-projeto)

---

## 1. Contexto do problema e solução

### Problema

Muitas pessoas não sabem para onde vai o próprio dinheiro, esquecem o vencimento das contas e não conseguem poupar. O controle costuma ficar em planilhas ou anotações soltas, sem uma visão consolidada de receitas, despesas e contas mês a mês. Planilhas exigem conhecimento de fórmulas, e os aplicativos prontos costumam ser complexos ou cheios de funções pagas.

**Persona:** Ana, 22 anos, estagiária. Quer saber quanto gasta com comida e descobrir quando já pode pagar uma viagem de R$ 6.000,00.

### Solução

O **Meu Bolso** é uma aplicação web para uma pessoa controlar o próprio dinheiro. Com ele será possível:

- criar conta, entrar e sair (senha guardada com hash bcrypt e acesso por token JWT) e excluir a conta com todos os dados (LGPD);
- cadastrar, consultar, alterar e excluir categorias de receita e de despesa (já existem categorias padrão);
- registrar receitas e despesas (lançamentos) e consultar o extrato do mês com filtros;
- cadastrar contas a pagar com vencimento (ex.: aluguel, água, luz), ver as atrasadas e as dos próximos 7 dias e marcá-las como pagas, o que gera a despesa automaticamente;
- definir um limite de gasto mensal por categoria, com alerta ao chegar em 90% e ao passar de 100%;
- cadastrar desejos (metas de compra) e ver quais já podem ser comprados com o saldo atual;
- ver um painel com saldo, receitas e despesas do mês e gráficos.

**Fora do escopo:** integração com bancos, contas recorrentes automáticas, cartão de crédito, alertas por e-mail e aplicativo móvel.

### Módulos e requisitos

| Módulo | Requisitos funcionais |
|---|---|
| Acesso | RF001 – RF005 |
| Categorias | RF006 – RF009 |
| Lançamentos | RF010 – RF013 |
| Contas a pagar | RF014 – RF018 |
| Orçamento | RF019 – RF020 |
| Metas | RF021 – RF024 |
| Painel | RF025 – RF027 |

A descrição completa de cada requisito está no [Documento de Requisitos](Requisitos/Meu_Bolso_Documento_de_Requisitos_v2.docx), na pasta `Requisitos/`.


### Protótipo das interfaces

O protótipo do Meu Bolso está disponível no Figma:

[Acessar o protótipo das interfaces](https://www.figma.com/design/5ttDYEP4jiga6eF7KJ71s4?node-id=4-1273)

A versão inicial apresenta telas de acesso, painel financeiro, extrato,
categorias, contas a pagar e desejos, além de formulários e confirmações.
As telas estão identificadas pelos nomes das interfaces e pelos códigos
dos requisitos funcionais relacionados.

Para explorar os fluxos, abra a tela I_Login no Figma e utilize a opção
de apresentação do protótipo. Os botões e menus conectam as telas.

O protótipo utiliza dados demonstrativos e não está conectado ao
back-end ou ao banco de dados. Ainda estão pendentes estados específicos
de edição, mensagens adicionais de erro, formulário de nova senha e
adaptações para telas menores.

---

## 2. Instruções para uso

Esta seção é para quem só quer **rodar o sistema** no próprio computador (por exemplo, um aluno de outra equipe), sem programar. Os comandos são para o **Prompt de Comando (cmd)** do Windows.

**Versão online:** `<link>`

### Passo a passo

1. **Instale os programas abaixo** (nas versões da seção [Tecnologias](#4-tecnologias)):
   - [Git](https://git-scm.com/downloads/win) 2.50.1
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Docker 29.9.2)
   - [Python](https://www.python.org/downloads/release/python-3135/) 3.13.5 – na instalação, marque **"Add python.exe to PATH"**.
   - [Node.js](https://nodejs.org/dist/v22.22.0/) 22.22.0 (o npm 10.9.4 já vem junto)

   Depois de instalar, feche e abra de novo o Prompt de Comando.

2. **Baixe o projeto**, de um destes dois jeitos:
   - **Com Git:** abra o Prompt de Comando na pasta onde quer guardar o projeto e rode:

     ```bat
     git clone https://github.com/samuelZ20/gestao_financeira.git
     cd gestao_financeira
     ```

   - **Sem Git:** na página do repositório no GitHub, clique em **Code > Download ZIP**, extraia o arquivo e abra o Prompt de Comando dentro da pasta extraída.

   > ⚠️ **Não coloque a pasta do projeto dentro do OneDrive** (nem em outra pasta sincronizada). A sincronização trava e corrompe as pastas `.venv` e `node_modules`. Use, por exemplo, `C:\projetos\gestao_financeira`.

3. **Suba o banco de dados.** Abra o **Docker Desktop** e espere aparecer "Engine running". Depois, na pasta do projeto:

   ```bat
   docker compose up -d
   ```

   Isso cria o container `meubolso-db` (PostgreSQL) na porta 5432.

4. **Prepare o back-end e crie as tabelas** (ainda na mesma janela):

   ```bat
   cd back-end
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env
   alembic upgrade head
   ```

5. **Inicie o back-end.** Na mesma janela (com o `.venv` ativado, aparece `(.venv)` no começo da linha):

   ```bat
   uvicorn app.main:app --reload
   ```

   Deixe essa janela aberta.

6. **Inicie o front-end.** Abra **outra** janela do Prompt de Comando na pasta do projeto e rode:

   ```bat
   cd front-end
   npm ci
   npm run dev
   ```

   Deixe essa janela aberta também.

7. **Abra o sistema no navegador:** <http://localhost:5173>. Deve aparecer a tela inicial do Meu Bolso. *(Enquanto as telas não forem implementadas, aparece a página padrão do Vite, com o título "Get started" e o botão "Count is 0".)*

### Como parar tudo

1. Em cada janela do back-end e do front-end, aperte **Ctrl + C** (se perguntar "Deseja finalizar o arquivo em lotes (S/N)?", digite `S`).
2. Para desligar o banco, na pasta do projeto:

   ```bat
   docker compose down
   ```

   Os dados continuam salvos no volume do Docker. Para usar de novo, repita o passo 3, depois `cd back-end`, `.venv\Scripts\activate` e o passo 5, e por fim o passo 6 (o `npm ci` pode ser pulado).

### Problemas comuns

| Problema | O que fazer |
|---|---|
| **Porta 5432 ocupada** (`Bind for 0.0.0.0:5432 failed: port is already allocated`) | Já existe outro PostgreSQL usando a porta. Pare o outro (serviço `postgresql` em *Serviços* do Windows ou outro container no Docker Desktop) e rode `docker compose up -d` de novo. |
| **Docker fechado** (`error during connect` ou `The system cannot find the file specified`) | Abra o Docker Desktop, espere "Engine running" e repita o comando. |
| **Erro ao ativar o `.venv`** | Use o **Prompt de Comando (cmd)**, não o PowerShell, e confira se você está dentro da pasta `back-end`. Se preferir o PowerShell, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e depois `.venv\Scripts\Activate.ps1`. |
| **"python" não é reconhecido como um comando** | O Python não foi adicionado ao PATH. Reinstale marcando **"Add python.exe to PATH"** e abra um novo Prompt de Comando. Como alternativa, use `py` no lugar de `python`. |
| **Porta 8000 ocupada** (`[WinError 10048]`) | Outro programa usa a porta 8000. Feche-o ou rode o back-end em outra porta: `uvicorn app.main:app --reload --port 8001`. |

---

## 3. Instruções para devs

### 3.1 Clonar o projeto

```bat
git clone https://github.com/samuelZ20/gestao_financeira.git
cd gestao_financeira
git checkout dev
```

> Não clone dentro do OneDrive (veja o aviso na [seção 2](#passo-a-passo)).

#### 3.1.1 Alternativa: baixar o ZIP

Na página do repositório, **Code > Download ZIP** e extraia. Sem o Git você não consegue fazer commit, então use essa opção só para consultar o código.

### 3.2 Instalar as dependências

Todos os comandos a partir da raiz do projeto, no Prompt de Comando.

```bat
REM Back-end: ambiente virtual e bibliotecas
cd back-end
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
cd ..

REM Front-end: bibliotecas exatamente como estão no package-lock.json
cd front-end
npm ci
cd ..

REM Banco de dados (Docker Desktop precisa estar aberto)
docker compose up -d

REM Tabelas do banco
cd back-end
alembic upgrade head
```

- O `.env` fica em `back-end\.env` e guarda a conexão com o banco (`DATABASE_URL`) e a chave do JWT (`SECRET_KEY`). Os valores do `.env.example` batem com o `docker-compose.yml`.
- **VS Code:** `Ctrl + Shift + P` > **Python: Select Interpreter** > escolha `back-end\.venv\Scripts\python.exe`.

### 3.3 Executar

O banco precisa estar ligado (`docker compose up -d`). Use duas janelas do Prompt de Comando, ambas a partir da raiz do projeto.

**Janela 1 – back-end:**

```bat
cd back-end
.venv\Scripts\activate
uvicorn app.main:app --reload
```

**Janela 2 – front-end:**

```bat
cd front-end
npm run dev
```

| O quê | URL | O que deve aparecer |
|---|---|---|
| Front-end | <http://localhost:5173> | A aplicação React do Meu Bolso (por enquanto, a página padrão do Vite: "Get started" e o botão "Count is 0") |
| API | <http://localhost:8000> | Respostas JSON da API |
| Documentação da API (Swagger) | <http://localhost:8000/docs> | Lista de rotas do FastAPI, que podem ser testadas pelo navegador |

### 3.4 Rodar os testes

Os testes ficam na pasta `teste/` (na raiz). Rode a partir de `back-end`, com o `.venv` ativado:

```bat
cd back-end
.venv\Scripts\activate
python -m pytest ..\teste\unidade --cov=app --cov-report=term-missing --cov-report=html:..\teste\cobertura
```

- O resumo da cobertura aparece no terminal e o relatório HTML é gerado em `teste\cobertura\index.html`.
- Use `python -m pytest` (e não só `pytest`) para que a pasta `back-end` entre no caminho do Python e o `import app` funcione nos testes.
- O coverage cria um `.gitignore` dentro de `teste\cobertura`. Para entregar o relatório, apague esse `.gitignore` antes do commit.

### 3.5 Rotina de trabalho e regras de Git

O fluxo completo está em [docs/GITFLOW.md](docs/GITFLOW.md). Resumo:

| Branch | Para que serve |
|---|---|
| `main` | Versões entregues (com tag `v1.0`, `v1.1`...). |
| `dev` | Integração do time. Base de todo o trabalho; deve estar sempre rodando. |
| `feature/*` | Uma tarefa (um RF). Nasce da `dev` e volta para a `dev` por pull request. |
| `hotfix/*` | Correção urgente na versão da `main`. Volta para a `main` e para a `dev`. |

**Rotina de cada tarefa:**

1. Antes de começar, atualize a `dev`:

   ```bat
   git checkout dev
   git pull origin dev
   ```

2. Crie a branch da tarefa com o código do requisito:

   ```bat
   git checkout -b feature/RF010-cadastrar-lancamento
   ```

3. Faça **commits pequenos**, com o código do RF na mensagem:

   ```bat
   git add .
   git commit -m "feat(RF010): rota de cadastro de lançamento"
   ```

4. **No fim do dia**, envie a branch para o GitHub:

   ```bat
   git push -u origin feature/RF010-cadastrar-lancamento
   ```

5. Ao terminar, traga as novidades da `dev` (`git pull origin dev`), resolva os conflitos e abra um **pull request para a `dev`**, revisado por **outro integrante**.

**Nunca:**

- commitar direto na `main` ou na `dev`;
- commitar `.env`, `.venv` ou `node_modules` (já estão no `.gitignore`).

### 3.6 Ao mudar dependências ou tabelas

- **Nova biblioteca Python:** com o `.venv` ativado, `pip install <pacote>` e depois atualize o arquivo:

  ```bat
  pip freeze > requirements.txt
  ```

- **Nova biblioteca do front-end:** `npm install <pacote>` dentro de `front-end`. Isso atualiza o `package.json` e o `package-lock.json`; commite os dois.
- **Mudança em tabela (model do SQLAlchemy):** gere e aplique a migração dentro de `back-end`:

  ```bat
  alembic revision --autogenerate -m "descricao da mudanca"
  alembic upgrade head
  ```

  Confira o arquivo gerado antes de commitar. Só uma pessoa por vez cria migração.

- **Avise o grupo.** Quem atualizar a `dev` depois precisa rodar `pip install -r requirements.txt`, `npm ci` e/ou `alembic upgrade head`.

---

## 4. Tecnologias

### Front-end

| Tecnologia | Versão | Uso |
|---|---|---|
| Node.js | 22.22.0 | Ambiente de execução JavaScript para o front-end |
| npm | 10.9.4 | Gerenciador de pacotes do front-end |
| React | 19.3.1 | Biblioteca de interface (componentes) |
| React DOM | 19.3.1 | Renderização do React no navegador |
| TypeScript | 7.0.2 | Tipagem estática do código do front-end |
| Vite | 8.3.5 | Servidor de desenvolvimento e build |
| @vitejs/plugin-react | 6.2.1 | Integração do React com o Vite |
| React Router DOM | 7.18.5 | Rotas/navegação entre páginas |
| Axios | 1.21.0 | Requisições HTTP para a API |
| Recharts | 3.10.1 | Gráficos do painel financeiro |
| Oxlint | 1.91.0 | Análise estática (lint) do código |

### Back-end

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.13.5 | Linguagem do back-end |
| FastAPI | 0.162.0 | Framework da API REST |
| Uvicorn (standard) | 0.54.0 | Servidor ASGI que executa a API |
| Pydantic | 2.14.2 | Validação de dados e schemas |
| pydantic-settings | 2.16.2 | Leitura de configurações/variáveis de ambiente |
| SQLAlchemy | 2.1.6 | ORM de acesso ao banco |
| Alembic | 1.20.1 | Migrações do banco de dados |
| psycopg (binary) | 3.3.7 | Driver de conexão com o PostgreSQL |
| bcrypt | 5.0.0 | Hash de senhas |
| PyJWT | 2.15.1 | Geração e validação de tokens JWT |

### Banco de dados

| Tecnologia | Versão | Uso |
|---|---|---|
| PostgreSQL | 17.11 (imagem `postgres:17.11`) | Banco de dados relacional |
| Docker Compose | v5.6.1 | Sobe o container do banco (`docker-compose.yml`) |

### Testes

| Tecnologia | Versão | Uso |
|---|---|---|
| pytest | 9.2.0 | Testes unitários e de integração |
| pytest-cov | 7.1.0 | Relatório de cobertura de testes |
| coverage | 7.17.1 | Medição de cobertura (usado pelo pytest-cov) |
| HTTPX | 0.28.1 | Cliente HTTP para testar a API (TestClient) |
| Selenium | 4.52.0 | Testes automatizados de interface (navegador) |

### Ferramentas

| Tecnologia | Versão | Uso |
|---|---|---|
| Visual Studio Code | 1.144.1 | IDE / editor de código |
| Git | 2.50.1 | Controle de versão |
| Docker | 29.9.2 | Execução do banco em container |
| Astah UML | preencher (Help > About) | Diagramas UML |
| GitHub Projects | serviço web (sem versão) | Quadro de tarefas das sprints |

### Como instalar as mesmas versões

As versões estão travadas em `back-end/requirements.txt` (todas com `==`), `front-end/package-lock.json` e na tag da imagem em `docker-compose.yml`. Depois de instalar Git, Python, Node.js e Docker nas versões acima, rode na raiz do projeto (Prompt de Comando):

```bat
cd back-end
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd ..\front-end
npm ci
cd ..
docker compose up -d
versoes.bat
```

Use `npm ci` (e não `npm install`): ele instala exatamente o que está no `package-lock.json`. No final, compare a saída do `versoes.bat` com as tabelas acima.

---

## 5. Organização do projeto

### Estrutura de pastas

*   **`back-end/`**: API em Python (FastAPI). Contém o `requirements.txt` e o `.env.example`.
    *   **`back-end/app/`**: código da aplicação; o `main.py` cria a aplicação FastAPI.
    *   **`back-end/app/core/`**: configurações gerais (leitura do `.env`, conexão com o banco, segurança/JWT).
    *   **`back-end/app/models/`**: modelos do SQLAlchemy (tabelas do banco).
    *   **`back-end/app/modules/`**: um módulo por área do sistema, cada um com `router.py` (rotas), `schemas.py` (validação com Pydantic) e `service.py` (regras de negócio).
        *   **`back-end/app/modules/acesso/`**: cadastro, login, logout e exclusão de conta (RF001–RF005).
        *   **`back-end/app/modules/categorias/`**: categorias de receita e despesa (RF006–RF009).
        *   **`back-end/app/modules/lancamentos/`**: receitas, despesas e extrato (RF010–RF013).
        *   **`back-end/app/modules/contas/`**: contas a pagar (RF014–RF018).
        *   **`back-end/app/modules/orcamento/`**: limite de gasto por categoria (RF019–RF020).
        *   **`back-end/app/modules/metas/`**: desejos/metas de compra (RF021–RF024).
        *   **`back-end/app/modules/painel/`**: dados do painel (RF025–RF027).
*   **`front-end/`**: interface em React + TypeScript (Vite). Contém `package.json`, `package-lock.json` e as configurações do Vite, do TypeScript e do Oxlint.
    *   **`front-end/context/`**: contextos globais do React (ex.: `AuthContext.tsx`, usuário logado e token).
    *   **`front-end/lib/`**: configuração de bibliotecas (ex.: `axios.ts`, cliente HTTP da API).
    *   **`front-end/routes/`**: definição das rotas/páginas (`AppRoutes.tsx`).
    *   **`front-end/shared/`**: código reaproveitado por vários módulos.
        *   **`front-end/shared/utils/`**: funções utilitárias (ex.: `formatCurrency.ts`).
    *   **`front-end/public/`**: arquivos estáticos servidos sem processamento (favicon, ícones).
    *   **`front-end/src/`**: ponto de entrada da aplicação (`main.tsx`, `App.tsx`) e estilos globais.
        *   **`front-end/src/assets/`**: imagens importadas pelo código.
        *   **`front-end/src/features/`**: uma pasta por módulo (`acesso`, `categorias`, `lancamentos`, `contas`, `orcamento`, `metas`, `painel`), cada uma com `components/` (telas e componentes), `hooks/` (lógica de estado) e `services/` (chamadas à API).
*   **`Requisitos/`**: documento de requisitos (`Meu_Bolso_Documento_de_Requisitos_v2.docx`), arquivos `.asta` dos diagramas UML e protótipo das telas.
*   **`Padroes Adotados/`**: padrões do grupo: regras de verificação e análise de requisitos, boas práticas de codificação e avaliação dos requisitos.
*   **`teste/`**: testes e validação.
    *   **`teste/validacao/`**: casos de teste de validação (com base nos requisitos).
    *   **`teste/unidade/`**: testes automatizados do back-end (pytest).
    *   **`teste/selenium/`**: scripts Selenium de teste da interface.
    *   **`teste/cobertura/`**: relatório de cobertura gerado pelo pytest-cov.
*   **`docs/`**: documentação do processo, como o [GITFLOW.md](docs/GITFLOW.md).
    *   **`docs/img/`**: imagens usadas na documentação (ex.: `gitflow.png`).
    *   **`docs/diagramas/`**: diagramas exportados (UML, arquitetura, banco de dados).

Arquivos na raiz: `docker-compose.yml` (container do PostgreSQL), `versoes.bat` (mostra as versões instaladas para comparar com a seção Tecnologias), `.gitignore` e este `README.md`.
