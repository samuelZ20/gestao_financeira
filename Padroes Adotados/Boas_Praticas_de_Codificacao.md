# Boas práticas de codificação do Meu Bolso

As seis práticas abaixo orientam a implementação e a revisão de pull requests do Meu Bolso. Os exemplos são do back-end Python com FastAPI, do front-end TypeScript com React e dos testes com Pytest.

## 1. Usar nomes claros e seguir a notação de cada linguagem

- **Python** — use `snake_case` para arquivos, funções e variáveis, `PascalCase` para classes e `UPPER_SNAKE_CASE` para constantes.
- **TypeScript e React** — use `camelCase` para funções, variáveis e hooks, com prefixo `use` nos hooks. Use `PascalCase` para tipos e componentes, incluindo os nomes de arquivos que exportam componentes.
- Preserve os nomes de campos que fazem parte do contrato da API, como `categoria_id`. Prefira verbos que descrevam a ação e nomes de domínio que identifiquem o dado.

**Aplicação no projeto** — `consultar_mes` e `RegraDeNegocioError` no [serviço de lançamentos](../back-end/app/modules/lancamentos/service.py), `registrarLancamento` no [cliente de lançamentos](../front-end/src/features/lancamentos/services/lancamentosService.ts) e `NovoLancamentoModal` no [componente de formulário](../front-end/src/features/lancamentos/components/NovoLancamentoModal.tsx).

## 2. Documentar decisões e regras de negócio

Use uma docstring curta em Python ou um comentário em TypeScript quando o código precisar explicar uma restrição, uma decisão ou uma regra de negócio. Inclua o identificador `RN` ou `RF` quando ele existir no documento de requisitos. Ao alterar a regra, revise o comentário junto com o código. Deixe atribuições e chamadas autoexplicativas com nomes claros.

**Aplicação no projeto** — a função `_validar_categoria_do_tipo` explica na docstring a RN02, que exige que receitas e despesas usem categorias do tipo correspondente. [Serviço de lançamentos](../back-end/app/modules/lancamentos/service.py)

## 3. Dar uma responsabilidade clara a cada camada

No back-end, use a rota para receber a requisição, acionar o serviço e definir a resposta HTTP. Coloque regras de negócio e operações da funcionalidade no serviço e mantenha os contratos de entrada e saída nos schemas. No front-end, mantenha os componentes focados na interação e concentre as chamadas HTTP do módulo em seu arquivo de serviço.

**Aplicação no projeto** — a rota `registrar_lancamento` chama `service.registrar`. No React, `NovoLancamentoModal` usa `registrarLancamento` do cliente da funcionalidade. [Rota](../back-end/app/modules/lancamentos/router.py) · [Serviço](../back-end/app/modules/lancamentos/service.py) · [Componente](../front-end/src/features/lancamentos/components/NovoLancamentoModal.tsx) · [Cliente HTTP](../front-end/src/features/lancamentos/services/lancamentosService.ts)

## 4. Tipar e validar as entradas e saídas da aplicação

Declare os tipos das entradas e dos retornos nos serviços e no cliente HTTP. Use os schemas do FastAPI para validar o formato recebido e mantenha no serviço as regras que dependem do domínio, como verificar se a categoria pertence ao usuário. No TypeScript, use os tipos da funcionalidade para representar formulários e respostas.

**Aplicação no projeto** — o cadastro recebe `LancamentoEntrada` e declara `LancamentoSaida` como resposta. O cliente usa `LancamentoForm` na entrada e `Promise<Lancamento>` no retorno. [Schemas](../back-end/app/modules/lancamentos/schemas.py) · [Rota](../back-end/app/modules/lancamentos/router.py) · [Cliente HTTP](../front-end/src/features/lancamentos/services/lancamentosService.ts)

## 5. Reutilizar regras compartilhadas

Quando duas operações aplicarem a mesma regra, mantenha a verificação em uma função com nome próprio e chame essa função em cada operação. Preserve o mesmo resultado e a mesma mensagem de erro para a mesma violação.

**Aplicação no projeto** — `registrar` e `alterar` usam `_buscar_categoria` e `_validar_categoria_do_tipo`. A verificação de titularidade e tipo fica centralizada. [Serviço de lançamentos](../back-end/app/modules/lancamentos/service.py)

## 6. Cobrir regras de negócio com testes verificáveis

Para cada regra criada ou alterada, cubra o comportamento esperado e uma entrada inválida ou condição de bloqueio, quando aplicável. Dê ao teste um nome que indique o cenário e o resultado esperado. Cada teste deve montar os próprios dados ou usar fixtures que os preparem.

**Aplicação no projeto** — os testes de lançamentos incluem o cadastro de uma despesa válida e a rejeição de valores inválidos e categorias de outro tipo. [Testes unitários de lançamentos](../teste/unidade/test_lancamentos.py)

## Revisão de pull request

- [ ] Nomes e notação seguem a linguagem e o contrato da API.
- [ ] Comentários e docstrings explicam regras ou decisões relevantes e estão atualizados.
- [ ] Rotas, serviços, schemas e componentes têm responsabilidades claras.
- [ ] Entradas e saídas têm tipos e validação apropriados.
- [ ] Regras repetidas foram reaproveitadas.
- [ ] O PR informa quais cenários foram testados e o resultado.
