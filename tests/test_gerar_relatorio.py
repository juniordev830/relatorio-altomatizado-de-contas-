import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gerar_relatorio import montar_html


def test_report_escapes_untrusted_category_values():
    malicious = '<script>alert("xss")</script>'
    frame = pd.DataFrame({"Produto": [malicious], "Total": [10.0]})

    html = montar_html(frame, {})

    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html
    assert "&lt;/script&gt;" in html



def test_load_data_discards_non_finite_amounts(monkeypatch):
    import gerar_relatorio

    frame = pd.DataFrame({
        "Produto": ["válido", "infinito", "negativo infinito", "ausente"],
        "Total": [12.5, float("inf"), float("-inf"), None],
    })
    monkeypatch.setattr(gerar_relatorio.pd, "read_excel", lambda *args, **kwargs: frame.copy())

    result = gerar_relatorio.carregar_dados("ignored.xlsx", 0)

    assert result["Produto"].tolist() == ["válido"]
    assert result["Total"].tolist() == [12.5]


def test_load_data_rejects_only_non_finite_amounts(monkeypatch):
    import pytest
    import gerar_relatorio

    frame = pd.DataFrame({"Produto": ["infinito"], "Total": [float("inf")]})
    monkeypatch.setattr(gerar_relatorio.pd, "read_excel", lambda *args, **kwargs: frame.copy())

    with pytest.raises(ValueError, match="não possui registros válidos"):
        gerar_relatorio.carregar_dados("ignored.xlsx", 0)


def test_parse_sheet_selector():
    import gerar_relatorio

    assert gerar_relatorio.parse_aba("2") == 2
    assert gerar_relatorio.parse_aba("Vendas") == "Vendas"

def test_validate_flag_skips_chart_generation_and_file_write(monkeypatch, tmp_path, capsys):
    import gerar_relatorio

    input_file = tmp_path / "dados.xlsx"
    input_file.write_bytes(b"teste")
    output_file = tmp_path / "relatorio.html"
    frame = pd.DataFrame({"Produto": ["A", "B", "A"], "Total": [10, 20, 30]})

    monkeypatch.setattr(gerar_relatorio, "carregar_dados", lambda *_: frame)
    monkeypatch.setattr(gerar_relatorio, "grafico_por_categoria",
                        lambda *_: (_ for _ in ()).throw(AssertionError("Não deveria gerar gráfico")))
    monkeypatch.setattr(sys, "argv", ["gerar_relatorio.py", str(input_file),
                                     "--validar", "--saida", str(output_file)])

    gerar_relatorio.main()

    assert not output_file.exists()
    assert "3 registros e 2 categorias" in capsys.readouterr().out
