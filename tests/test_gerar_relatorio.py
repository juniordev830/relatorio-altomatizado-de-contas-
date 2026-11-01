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
