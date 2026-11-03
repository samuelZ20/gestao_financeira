@echo off
REM Mostra as versoes de todas as ferramentas e bibliotecas do projeto Meu Bolso.
REM Uso: rode "versoes.bat" na raiz do projeto e compare a saida com a tabela do README.
setlocal
cd /d "%~dp0"

echo ===== Ferramentas =====
echo [Git]
git --version
echo [Python]
python --version
echo [Node.js]
node --version
echo [npm]
call npm --version
echo [Docker]
docker --version
echo [Docker Compose]
docker compose version
echo [VS Code]
call code --version

echo.
echo ===== Banco de dados (container "db") =====
docker compose exec -T db postgres --version
if errorlevel 1 echo Container nao esta rodando. Execute: docker compose up -d

echo.
echo ===== Back-end (back-end\.venv) =====
if exist "back-end\.venv\Scripts\python.exe" (
    "back-end\.venv\Scripts\python.exe" --version
    "back-end\.venv\Scripts\python.exe" -m pip freeze
) else (
    echo Ambiente virtual nao encontrado. Veja a secao Tecnologias do README.
)

echo.
echo ===== Front-end (front-end\node_modules) =====
if exist "front-end\node_modules" (
    pushd front-end
    call npm ls --depth=0
    popd
) else (
    echo node_modules nao encontrado. Rode: cd front-end ^&^& npm ci
)

endlocal
