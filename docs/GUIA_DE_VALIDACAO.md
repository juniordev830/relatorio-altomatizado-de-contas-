# Guia de verificação e manutenção

O projeto lê uma planilha Excel e gera um HTML com indicadores, gráficos e resumo por categoria. A versão adaptada para lançamentos PJ também está em `auxiliar-NF-pj/relatorios/`; manter esta implementação como referência original, evitando divergência silenciosa.

## Rotina reproduzível

```bash
python -m pip install -r requirements.txt
python gerar_relatorio.py vendas_exemplo.xlsx --saida relatorio.html
python -m pytest tests -q
```

Abra o HTML gerado no navegador e confirme que tabelas, valores e gráficos correspondem à planilha de entrada.

## Casos de teste relevantes

- Planilha sem `Produto` ou `Total` deve explicar quais colunas faltam.
- Dados vazios, infinitos e não numéricos não podem gerar gráficos enganosos.
- Datas ausentes não devem produzir uma série temporal inventada.
- Valores negativos ou soma zero devem desativar a interpretação percentual em pizza.
- Texto vindo de células deve ser escapado no HTML, especialmente rótulos de categorias.
- Compare um arquivo Excel pequeno com soma manual antes de aceitar relatórios grandes.

## Evolução sugerida

Separar regras de limpeza, agregação e apresentação em módulos testáveis; permitir nomes de colunas parametrizados via CLI; padronizar exemplos sintéticos e aumentar testes de entradas inválidas. Nunca versionar planilhas de clientes ou relatórios com dados pessoais.
