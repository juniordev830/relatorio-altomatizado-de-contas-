# Relatório automatizado de contas

Gera um relatório HTML com indicadores, gráficos e tabela-resumo a partir de uma planilha `.xlsx`.

## Como executar

```bash
python -m pip install -r requirements.txt
python gerar_relatorio.py vendas_exemplo.xlsx --saida relatorio.html
```

O script valida as colunas configuradas, descarta linhas inválidas e informa erros de entrada sem gerar um relatório incompleto. Para usar outros nomes de colunas, ajuste `COLUNA_DATA`, `COLUNA_CATEGORIA` e `COLUNA_VALOR` no início de `gerar_relatorio.py`.

O arquivo de exemplo `vendas_exemplo.xlsx` é mantido no repositório para facilitar a validação local.
