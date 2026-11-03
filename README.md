# gestao_financeira

## Tecnologias

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
