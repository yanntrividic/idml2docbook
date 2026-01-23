# tests/test_idml2docbook.py
from pathlib import Path
import pytest
from idml2docbook.core import idml2docbook
from idml2docbook import DEFAULT_OPTIONS

TESTDATA = Path("tests")

FILES = [
    ("hello_world/hello_world.idml", "hello_world/hello_world.dbk"),
    ("package/Package_test/test.idml", "package/test.dbk")
]

@pytest.mark.parametrize("files", FILES)
def test_convert_idml_to_docbook(files):
    idml_name, dbk_name = files

    idml_path = TESTDATA / idml_name
    dbk_path = TESTDATA / dbk_name

    assert idml_path.exists(), f"Missing input file: {idml_path}"
    assert dbk_path.exists(), f"Missing expected file: {dbk_path}"

    expected_docbook = dbk_path.read_text(encoding="utf-8")

    processed_docbook = idml2docbook(str(idml_path), **DEFAULT_OPTIONS)
    
    assert expected_docbook == processed_docbook
