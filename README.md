# Relatório Automatizado de Contas

Aplicação Python que gera um relatório HTML com indicadores, gráficos e uma tabela-resumo a partir de uma planilha Excel (.xlsx).

## Funcionalidades

- Lê dados de uma planilha de entrada.
- Valida as colunas configuradas e trata linhas inválidas.
- Gera um relatório HTML para consulta no navegador.
- Mantém uma planilha de exemplo para facilitar a execução local.

## Requisitos

- Python 3
- Dependências listadas em `requirements.txt`

## Instalação

```bash
python -m venv .venv
```

Ative o ambiente virtual:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Gerar um relatório

Com a planilha de exemplo:

```bash
python gerar_relatorio.py vendas_exemplo.xlsx --saida relatorio.html
```

Abra o arquivo `relatorio.html` gerado no navegador. Para usar outra planilha, passe o caminho do arquivo como primeiro argumento.

## Configuração das colunas

Os nomes das colunas esperadas estão configurados no início de `gerar_relatorio.py`. Ajuste `COLUNA_DATA`, `COLUNA_CATEGORIA` e `COLUNA_VALOR` para corresponder ao cabeçalho do seu arquivo.

Confira se a planilha contém os dados esperados antes de gerar o relatório. O script valida entradas e informa problemas de leitura para evitar produzir um relatório incompleto silenciosamente.

## Estrutura

```text
.
├── gerar_relatorio.py
├── requirements.txt
├── vendas_exemplo.xlsx
├── relatorio.html              # exemplo/saída HTML versionada
├── documentacao_projeto.docx
└── README.md
```

## Limitações e melhorias futuras

- Adicionar testes automatizados para arquivos válidos e inválidos.
- Permitir configurar as colunas por argumentos de linha de comando.
- Adicionar mensagens de validação mais detalhadas e exportação em outros formatos.

O arquivo de exemplo contém dados demonstrativos; substitua-o por dados autorizados e evite publicar informações financeiras pessoais ou confidenciais.

## Validação e manutenção

Para revisar alterações neste projeto, consulte o [guia técnico de validação](docs/GUIA_DE_VALIDACAO.md), com comandos, cenários de regressão e próximos incrementos.
