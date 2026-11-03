# Regras de Verificação e Analise de Requisitos

**GCC 188 – Engenharia de Software**

Projeto Meu Bolso. Versão 2.0, 03/11/2026. Pasta: Padrões Adotados.

## 1. Objetivo e fonte

Este documento define as regras que o Documento de Requisitos do Meu Bolso deve obedecer. Cada regra tem um critério que pode ser contado ou conferido, de modo que duas pessoas diferentes chegam ao mesmo resultado. As regras valem para requisitos funcionais (RF), requisitos não funcionais (NF) e regras de negócio (RN), e são aplicadas pela equipe na verificação dos requisitos (tarefa #16).

**Livro de referência:** MAGELA, Rogério. Engenharia de Software Aplicada: Fundamentos. Alta Books. As regras VR01 a VR09 foram retiradas do Capítulo 1 (Análise de Requisitos), principalmente das seções 7.2 (Especificação de Requisitos) e 7.3 (Análise de Requisitos). A regra VR10 vem da planilha de tarefas do professor. Os números de página são os impressos no capítulo.

## 2. Nomenclatura adotada

- **RF:** requisito funcional, seguido de 3 dígitos (RF001, RF002...).
- **NF:** requisito não funcional, seguido de 3 dígitos (NF001, NF002...).
- **RN:** regra de negócio, seguida de 2 dígitos (RN01, RN02...).
- **Interfaces:** "I_" para interface, "IE_" para interface com mensagem de erro e "IS_" para interface com mensagem de sucesso, seguido de nome sem espaços (`I_Login`, `IE_LoginCredenciaisInvalidas`).
- **Prioridade:** exatamente uma entre Essencial, Importante e Desejável, que correspondem a Crítico, Importante e Útil do atributo Benefício do livro (seção 5.1, p. 11).

## 3. Regras de verificação

Cada regra traz o critério mensurável, a forma de verificar e a seção do livro de onde vem.

| ID | Regra | Critério mensurável | Como verificar | Fonte |
| --- | --- | --- | --- | --- |
| **VR01** | **Identificador único** | Todo RF, NF e RN tem identificador no formato da seção 2. Nenhum identificador aparece em dois requisitos. Nenhum número é reaproveitado depois de excluído. | Listar os identificadores e conferir formato e duplicidade (esperado: 0 duplicados, 0 fora do formato). | Cap. 1, seção 7.3.9 (Rastreável para frente), p. 22: requisitos identificados de forma única. |
| **VR02** | **Um requisito por vez** | O nome de cada RF e de cada NF não contém as palavras E, OU nem MAS. O nome de cada RF tem um único verbo, o do infinitivo inicial. | Buscar as três palavras nos nomes (esperado: 0 ocorrências) e contar os verbos do nome de cada RF (esperado: 1). | Cap. 1, seção 7.2.1, p. 18 (Defina somente um requisito por vez) e seção 7.2.2, p. 18. |
| **VR03** | **Palavras evitadas** | Nenhum texto de requisito (nome, resumo, descrição, fluxos e regras) contém: SOMENTE SE, EXCETO, SE NECESSÁRIO, CONTUDO, ENTRETANTO, USUALMENTE, GERALMENTE, FREQUENTEMENTE, TIPICAMENTE, AMIGÁVEL, VERSÁTIL, FLEXÍVEL, APROXIMADAMENTE, TÃO LOGO QUANTO POSSÍVEL, TALVEZ, PROVAVELMENTE. As palavras E, OU e MAS, da mesma lista do livro, são controladas apenas nos nomes (VR02), porque os fluxos as usam naturalmente. | Buscar cada expressão no documento (esperado: 0 ocorrências nos capítulos de requisitos). | Cap. 1, seção 7.2.2 (Evite as palavras), p. 18. |
| **VR04** | **Frases curtas** | O resumo de cada RF tem uma única frase (um único ponto final) e no máximo 25 palavras. O limite de 25 foi escolhido pela equipe. | Contar palavras e pontos finais do campo Resumo (esperado: 1 ponto, até 25 palavras). | Cap. 1, seção 7.2.3 (Evite frases grandes), p. 18. |
| **VR05** | **Vocabulário fechado** | Todo termo de domínio usado nos requisitos (lançamento, receita, despesa, categoria, conta a pagar, orçamento, desejo, saldo) está definido no glossário da seção 1.2. Cada conceito usa um único termo: sinônimos (ex.: transação, meta, conta fixa) só aparecem no glossário, remetidos ao termo principal. | Buscar cada termo e cada sinônimo (esperado: os sinônimos aparecem apenas no glossário). | Cap. 1, seção 7.2.4, p. 18 (vocabulário fechado) e seção 7.3.5 (Consistente), p. 21. |
| **VR06** | **Requisito não funcional verificável** | Todo NF contém ao menos um destes itens: número com unidade (ex.: 3 segundos), percentual, versão de tecnologia (ex.: Python 3.12) ou formato literal (ex.: DD/MM/AAAA). Toda tecnologia citada vem com versão. | Conferir cada NF contra os quatro itens; procurar nomes de tecnologia sem versão ao lado. | Cap. 1, seção 7.3.4 (Verificável), p. 21; seções 3.4 e 3.6, p. 8 (ex.: tempo máximo de dez segundos). |
| **VR07** | **Origem registrada (rastreável para trás)** | Todo RF e todo NF tem a origem registrada na coluna Fonte da tabela de rastreabilidade (quem pediu ou documento de origem, ex.: Enunciado do Projeto Final). | Contar as linhas com Fonte preenchida (esperado: 100% dos requisitos). | Cap. 1, seção 7.3.8 (Rastreável para trás), p. 22; seção 5.3 (Fonte), p. 12. |
| **VR08** | **Rastreável para frente** | Todo RF tem: (a) um caso de uso de nome idêntico no diagrama; (b) pelo menos 1 interface no campo Interfaces; (c) pelo menos 1 issue no Kanban com o código do RF no título. Todo NF indica os casos de uso associados ou "todo o sistema". | Para cada RF, marcar a, b e c (esperado: 100% com as três marcações). | Cap. 1, seção 7.3.9, p. 22; seção 4, p. 9 (cada caso de uso corresponde a um requisito funcional); seção 7.2.9, p. 19. |
| **VR09** | **Prioridade definida** | Todo RF e todo NF tem exatamente uma prioridade marcada entre Essencial, Importante e Desejável. | Contar as marcações por requisito (esperado: 1 por requisito). | Cap. 1, seção 5.1 (Benefício), p. 11. |
| **VR10** | **Pré-condição com login e tela** | Todo RF que exige usuário logado traz na pré-condição a frase "O usuário deve estar logado no sistema." e uma frase com a tela de origem, usando o nome de uma interface que existe no protótipo. | Conferir o campo Pré-condição de cada RF e comparar o nome da tela com a lista de interfaces. | Planilha de tarefas do professor, tarefa #12 (não é do livro). |

*Observação sobre VR01: o livro também pede identificação hierárquica (ex.: URQ1 e URQ1.1). Este projeto não usa requisitos filhos, então os identificadores são planos.*

## 4. Como aplicar

- Cada integrante verifica os requisitos dos seus módulos, conforme a divisão da equipe.
- Para cada requisito e cada regra, registra "Atende" ou "Não atende" em uma tabela de avaliação (modelo abaixo).
- O que "Não atende" é corrigido no documento e verificado de novo. A tabela final, sem pendências, é guardada em Padrões Adotados.
- Um colega revisa a avaliação feita pelo outro antes de ela ser considerada concluída. O livro recomenda que a análise seja feita por outra pessoa, e não por quem especificou (seção 7.3, p. 19).
- Ao mudar o documento de requisitos depois da primeira versão, as regras são aplicadas de novo apenas aos requisitos alterados.

### Modelo da tabela de avaliação

| Requisito | VR01 | VR02 | VR03 | VR04 | VR05 | VR06 | VR07 | VR08 | VR09 | VR10 | Observação |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RF001 |  |  |  |  |  | — |  |  |  |  |  |
| NF001 |  |  |  | — |  |  |  |  |  | — |  |

*O traço indica que a regra não se aplica ao tipo do requisito (VR04 e VR10 valem só para RF; VR06 só para NF).*
