![PyPI - Version](https://img.shields.io/pypi/v/idml2docbook)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/yanntrividic/idml2docbook/publish.yml)
![GitHub License](https://img.shields.io/github/license/yanntrividic/idml2docbook)

# idml2docbook

This Python package converts IDML (InDesign Markup Language) files to Docbook 5.1.

It is wrapper around [idml2xml-frontend](https://github.com/transpect/idml2xml-frontend) that takes the output file and converts it to Docbook 5.1.

## Installation

First, [create a virtual environment](https://www.w3schools.com/python/python_virtualenv.asp).
Then, you can install and download this package using `pip`:

```
pip install idml2docbook
```

The package is now installed, but the environment still needs to be configured. This converter requires external dependencies, namely:

* python > 3.0.0
* java > 1.7
* bash > 5
* git (to install idml2xml-frontend)
* idml2xml-frontend

The following command helps you check if you have those dependencies installed. It also installs idml2xml-frontend and generates a sample `.env` if none are to be found in your folder:

```
idml2docbook-install-dependencies
```

> **Note:** If you already have a `.env` file in your project, you will need to manually add it the path to idml2xml-frontend:

```
IDML2HUBXML_SCRIPT_FOLDER="/path/to/idml2xml-frontend"
```

## Usage

### Command-line

Convert an IDML file:

```bash
idml2docbook file.idml
```

Options are also available. They are as well documented in the command-line tool (see the help with `-h`/`--help`).

* **`-x`, `--idml2hubxml-file`** \
    Treats the input file as a Hub XML file. \
    Useful for saving processing time if `idml2xml-frontend` has already been run on the source IDML file.

* **`-o`, `--output <fichier>`** \
    Name to assign to the output file. \
    By default, output is sent to standard output (stdout).

* **`-t`, `--typography`** \
    Applies French typographic refinements. \
    (thin spaces, non-breaking spaces, etc.).

* **`-l`, `--thin-spaces`** \
    Use only thin spaces for typography refinement. \
    Should be used together with `--typography`.

* **`-b`, `--linebreaks`** \
    Do not replace `<br>` tags with spaces.

* **`-f`, `--media <chemin>`** \
    Path to the folder containing media files. \
    Default: `Links`.

* **`-r`, `--raster <extension>`** \
    Extension to use when replacing that of raster images. \
    Example: `jpg`.

* **`-v`, `--vector <extension>`** \
    Extension to use when replacing that of vector images. \
    Example: `svg`.

* **`-i`, `--idml2hubxml-output <chemin>`** \
    Path to the output from Transpect’s idml2hubxml converter. \
    Default: `idml2hubxml`.

* **`-s`, `--idml2hubxml-script <chemin>`** \
    Path to the script of Transpect’s idml2xml-frontend converter.

* **`--version`** \
    Displays the version of idml2docbook and exits the program.

> **Note:** For large IDML files, it may be necessary to [increase the Java heap size](https://github.com/transpect/idml2xml-frontend/blob/master/idml2xml.sh#L33), for example to `2048m` or `4096m`.

### Python script

Here is sample script for how to use the API:

```python
from idml2docbook.core import idml2docbook

myfile = "file.idml"

# Options are optional!
options = {
    'typography': True,
    'thin_spaces': True,
    'linebreaks': True,
    'ignore_overrides': True,
    'raster': "jpg",
    'vector': "svg",
    'media': "images"
}

output = idml2docbook(myfile, **options)
print(output)
```

