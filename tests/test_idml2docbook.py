# tests/test_idml2docbook.py
from pathlib import Path
import pytest
from idml2docbook.core import idml2docbook
from idml2docbook import DEFAULT_OPTIONS

TESTDATA = Path("tests")

FILES = [
    {
        "idml": "hello_world/hello_world.idml",
        "hubxml": "hello_world/hello_world.xml",
        "dbk": "hello_world/hello_world.dbk"
    },
    {
        "idml": "package/Package_test/test.idml",
        "hubxml": "package/Package_test/test.xml",
        "dbk": "package/test.dbk"
    }
]

@pytest.mark.parametrize("files", FILES)
def test_convert_idml_to_docbook(files):
    idml_path = TESTDATA / files["idml"]
    dbk_path = TESTDATA / files["dbk"]

    assert idml_path.exists(), f"Missing input file: {idml_path}"
    assert dbk_path.exists(), f"Missing expected file: {dbk_path}"

    expected_docbook = dbk_path.read_text(encoding="utf-8")
    processed_docbook = idml2docbook(str(idml_path), **DEFAULT_OPTIONS)
    
    assert expected_docbook == processed_docbook

BOLLO = {
    "hubxml": "bollo/bollo.xml",
    "dbk": "bollo/bollo.dbk"
}

def test_convert_bollo():
    options = DEFAULT_OPTIONS.copy()

    options['idml2hubxml_file'] = BOLLO["hubxml"]
    options['typography'] = True
    options['thin_spaces'] = True
    options['ignore_overrides'] = True
    options['thin_spaces'] = True
    options['raster'] = "jpg"
    options['vector'] = "svg"
    options['media'] = "images"

    hubxml_path = TESTDATA / BOLLO["hubxml"]
    dbk_path = TESTDATA / BOLLO["dbk"]

    assert hubxml_path.exists(), f"Missing input file: {hubxml_path}"
    assert dbk_path.exists(), f"Missing expected file: {dbk_path}"

    expected_docbook = dbk_path.read_text(encoding="utf-8")
    processed_docbook = idml2docbook(str(hubxml_path), **options)

    assert expected_docbook == processed_docbook