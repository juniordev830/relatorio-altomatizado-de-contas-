import pandas as pd

from gerar_relatorio import montar_html


def test_report_escapes_untrusted_category_values():
    malicious = '<script>alert("xss")</script>'
    frame = pd.DataFrame({"Produto": [malicious], "Total": [10.0]})

    html = montar_html(frame, {})

    assert "<script>alert" not in html
    assert "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;" in html
