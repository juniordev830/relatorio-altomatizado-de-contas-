"""
Automação: gera um relatório em HTML (com gráficos) a partir de uma planilha Excel.

COMO USAR
---------
1. Instale as dependências (uma vez só):
   pip install pandas openpyxl matplotlib --break-system-packages

2. Ajuste as configurações na seção "CONFIGURAÇÕES" abaixo:
   - ARQUIVO_ENTRADA: caminho do seu .xlsx
   - COLUNA_DATA, COLUNA_CATEGORIA, COLUNA_VALOR: nomes das colunas na sua planilha

3. Rode:
   python gerar_relatorio.py

O script gera "relatorio.html" na mesma pasta, com resumo estatístico e gráficos.
"""

import pandas as pd
import argparse
from html import escape
import matplotlib
matplotlib.use("Agg")  # não precisa de interface gráfica
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import base64
from io import BytesIO

# ============================================================
# CONFIGURAÇÕES — ajuste aqui para a sua planilha
# ============================================================
ARQUIVO_ENTRADA = "vendas_exemplo.xlsx"   # caminho do seu arquivo .xlsx
ABA = 0                                   # nome ou índice da aba (0 = primeira)

COLUNA_DATA = "Data"                      # coluna com datas (ou None se não tiver)
COLUNA_CATEGORIA = "Produto"              # coluna categórica principal (ex: produto, região)
COLUNA_VALOR = "Total"                    # coluna numérica a somar/analisar

ARQUIVO_SAIDA = "relatorio.html"
# ============================================================


def carregar_dados(caminho: str, aba) -> pd.DataFrame:
    """Lê a planilha e faz limpeza básica."""
    df = pd.read_excel(caminho, sheet_name=aba)

    required = [column for column in (COLUNA_CATEGORIA, COLUNA_VALOR) if column]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(missing)}")

    # remove linhas totalmente vazias
    df = df.dropna(how="all")
    df[COLUNA_VALOR] = pd.to_numeric(df[COLUNA_VALOR], errors="coerce")
    df = df.dropna(subset=[COLUNA_CATEGORIA, COLUNA_VALOR])
    if df.empty:
        raise ValueError("A planilha não possui registros válidos após a limpeza.")

    # converte a coluna de data, se existir
    if COLUNA_DATA and COLUNA_DATA in df.columns:
        df[COLUNA_DATA] = pd.to_datetime(df[COLUNA_DATA], errors="coerce")

    return df


def fig_para_base64(fig) -> str:
    """Converte uma figura matplotlib em string base64 para embutir no HTML."""
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=110)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def grafico_por_categoria(df: pd.DataFrame) -> str:
    """Gráfico de barras: soma do valor por categoria."""
    resumo = df.groupby(COLUNA_CATEGORIA)[COLUNA_VALOR].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    resumo.plot(kind="bar", ax=ax, color="#4C72B0")
    ax.set_title(f"{COLUNA_VALOR} total por {COLUNA_CATEGORIA}")
    ax.set_ylabel(COLUNA_VALOR)
    ax.set_xlabel(COLUNA_CATEGORIA)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig_para_base64(fig)


def grafico_temporal(df: pd.DataFrame) -> str | None:
    """Gráfico de linha: evolução do valor ao longo do tempo (se houver coluna de data)."""
    if not COLUNA_DATA or COLUNA_DATA not in df.columns:
        return None

    serie = df.groupby(pd.Grouper(key=COLUNA_DATA, freq="MS"))[COLUNA_VALOR].sum()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    serie.plot(kind="line", marker="o", ax=ax, color="#DD8452")
    ax.set_title(f"Evolução mensal de {COLUNA_VALOR}")
    ax.set_ylabel(COLUNA_VALOR)
    ax.set_xlabel("Período")
    plt.tight_layout()
    return fig_para_base64(fig)


def grafico_pizza(df: pd.DataFrame) -> str:
    """Gráfico de pizza: participação percentual por categoria."""
    resumo = df.groupby(COLUNA_CATEGORIA)[COLUNA_VALOR].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(resumo, labels=resumo.index, autopct="%1.1f%%", startangle=90)
    ax.set_title(f"Participação de {COLUNA_VALOR} por {COLUNA_CATEGORIA}")
    plt.tight_layout()
    return fig_para_base64(fig)


def montar_html(df: pd.DataFrame, imgs: dict) -> str:
    """Monta o relatório HTML final."""
    total = df[COLUNA_VALOR].sum()
    media = df[COLUNA_VALOR].mean()
    qtd_registros = len(df)
    top_categoria = df.groupby(COLUNA_CATEGORIA)[COLUNA_VALOR].sum().idxmax()

    tabela_resumo = (
        df.groupby(COLUNA_CATEGORIA)[COLUNA_VALOR]
        .agg(["sum", "mean", "count"])
        .rename(columns={"sum": "Total", "mean": "Média", "count": "Registros"})
        .sort_values("Total", ascending=False)
        .round(2)
        .to_html(classes="tabela")
    )

    blocos_grafico = ""
    for titulo, img_b64 in imgs.items():
        if img_b64:
            blocos_grafico += f"""
            <div class="grafico">
                <h2>{titulo}</h2>
                <img src="data:image/png;base64,{img_b64}" alt="{titulo}">
            </div>
            """

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<title>Relatório de Dados</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 40px; color: #222; background: #f7f7f9; }}
    h1 {{ color: #2c3e50; }}
    h2 {{ color: #34495e; margin-top: 30px; }}
    .cards {{ display: flex; gap: 20px; margin: 20px 0 40px 0; flex-wrap: wrap; }}
    .card {{ background: white; border-radius: 10px; padding: 20px 25px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); min-width: 160px; }}
    .card .valor {{ font-size: 24px; font-weight: bold; color: #4C72B0; }}
    .card .label {{ font-size: 13px; color: #777; margin-top: 4px; }}
    .grafico {{ background: white; border-radius: 10px; padding: 20px; margin-bottom: 25px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }}
    .grafico img {{ max-width: 100%; }}
    table.tabela {{ border-collapse: collapse; width: 100%; background: white; }}
    table.tabela th, table.tabela td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: right; }}
    table.tabela th {{ background: #4C72B0; color: white; }}
    table.tabela td:first-child, table.tabela th:first-child {{ text-align: left; }}
    footer {{ margin-top: 40px; font-size: 12px; color: #999; }}
</style>
</head>
<body>
    <h1>Relatório de Dados</h1>
    <p>Gerado a partir de <b>{escape(ARQUIVO_ENTRADA)}</b> em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>

    <div class="cards">
        <div class="card"><div class="valor">{total:,.2f}</div><div class="label">Total ({COLUNA_VALOR})</div></div>
        <div class="card"><div class="valor">{media:,.2f}</div><div class="label">Média ({COLUNA_VALOR})</div></div>
        <div class="card"><div class="valor">{qtd_registros}</div><div class="label">Registros</div></div>
        <div class="card"><div class="valor">{top_categoria}</div><div class="label">Top {COLUNA_CATEGORIA}</div></div>
    </div>

    {blocos_grafico}

    <h2>Tabela resumo por {COLUNA_CATEGORIA}</h2>
    {tabela_resumo}

    <footer>Relatório gerado automaticamente via script Python.</footer>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Gera um relatório HTML a partir de uma planilha Excel.")
    parser.add_argument("arquivo", nargs="?", default=ARQUIVO_ENTRADA, help="Caminho do arquivo .xlsx")
    parser.add_argument("--saida", default=ARQUIVO_SAIDA, help="Caminho do HTML gerado")
    args = parser.parse_args()

    caminho = Path(args.arquivo)
    if not caminho.exists():
        parser.error(f"Arquivo não encontrado: {caminho}")

    print(f"Lendo {ARQUIVO_ENTRADA} ...")
    try:
        df = carregar_dados(str(caminho), ABA)
    except ValueError as error:
        parser.error(str(error))
    print(f"{len(df)} linhas carregadas.")

    print("Gerando gráficos...")
    imgs = {
        f"Total por {COLUNA_CATEGORIA}": grafico_por_categoria(df),
        "Evolução no tempo": grafico_temporal(df),
        f"Participação por {COLUNA_CATEGORIA}": grafico_pizza(df),
    }

    print("Montando relatório...")
    html = montar_html(df, imgs)

    Path(args.saida).write_text(html, encoding="utf-8")
    print(f"Relatório salvo em: {args.saida}")


if __name__ == "__main__":
    main()
