import sys
from pathlib import Path
# Add project root to Python path so pytest can import app.py
# when tests are executed from the tests/ subfolder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_vulnerable_endpoint_reflects_script_tag(client):
    payload = "<script>alert('XSS!')</script>"
    resp = client.get("/search-vuln", query_string={"q": payload})
    assert resp.status_code == 200
    # In the vulnerable view, the script tag should be present as-is
    assert payload in resp.get_data(as_text=True)


def test_fixed_endpoint_escapes_script_tag(client):
    payload = "<script>alert('XSS!')</script>"
    resp = client.get("/search-fixed", query_string={"q": payload})
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)

    # Script tag should be escaped, not present literally
    assert "<script>" not in html
    assert "</script>" not in html
    assert "&lt;script&gt;" in html
    assert "&lt;/script&gt;" in html
