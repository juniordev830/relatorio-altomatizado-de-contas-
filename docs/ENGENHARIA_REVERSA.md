# Engenharia reversa e estudo — Relatório Automatizado de Contas

## Objetivo e fluxo

Relatório local de despesas a partir de Excel. A CLI lê a planilha, consolida os valores por data e categoria e incorpora os gráficos ao HTML. Em gerar_relatorio.py, acompanhe carregar_dados, parse_aba e montar_html.

**Tecnologias identificadas** · Python.

**Revisão de referência** · `b5b74d94b8d8`.

## Mapa do código

| Caminho | Papel de leitura | Símbolos selecionados |
| --- | --- | --- |
| [gerar_relatorio.py](../gerar_relatorio.py) | Implementação | `carregar_dados`, `fig_para_base64`, `grafico_por_categoria`, `grafico_temporal`, `grafico_pizza`, `parse_aba`, `montar_html`, `main` |
| [relatorio.html](../relatorio.html) | Marcação ou estilos da interface | — |

## Configuração e referências

Ambiente e dependências: [requirements.txt](../requirements.txt).

Referências existentes: [docs/GUIA_DE_VALIDACAO.md](GUIA_DE_VALIDACAO.md).

## Roteiro de estudo e desenvolvimento

1. Comece pelo fluxo descrito acima e localize seus pontos de entrada no mapa. Acompanhe uma entrada válida até a transformação ou a resposta.
2. Abra um teste relacionado ao fluxo e descreva qual regra ele protege. Compare o tratamento esperado para entradas válidas, inválidas e nos limites.
3. Ao adicionar uma regra, determine qual módulo controla o dado e cubra o caso nesse nível. Em seguida, confira o efeito no comando, na API ou na interface de entrada.

**Pergunta de entrevista**

Onde incluiria a validação de uma coluna monetária sem acoplar a regra ao HTML?

## Testes versionados

Arquivos para começar a leitura dos cenários de teste: [tests/test_chart_edge_cases.py](../tests/test_chart_edge_cases.py), [tests/test_gerar_relatorio.py](../tests/test_gerar_relatorio.py).

Os comandos e versões de runtime usados no CI ficam em [.github/workflows/ci.yml](../.github/workflows/ci.yml), [.github/workflows/portfolio-checks.yml](../.github/workflows/portfolio-checks.yml).

[Voltar ao README](../README.md).
