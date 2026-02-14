# Revision history for idml2docbook

## idml2docbook 1.1.6 (2026-02-14)

* The README refers to Pandoc 3.9 as a fully compatible version (support of `role` attributes).
* The `.env` file exposes a variable to customise the path to a specific `bash` version. Particularly useful for macOS, where the default `bash` version is not compatible.
* Java version check is now robust to the change of semantic versioning between 1.8 and 9.

## idml2docbook 1.1.4 (2026-01-26)

* Writing some docs in `README.md`.
* Installation script now checks for bash version.
* Cleaning `idml2hubxml.py`
* bash calls are now forced on idml2hubxml-frontend.
* Fixing packaging bugs.

## idml2docbook 1.1.0 (2026-01-26)

* Added unit tests in the `tests` folder.
* Better formatter for output Docbook files.
* `-p`/`--prettify` option removed as there is an okay formatting by default, and this option most of the times broke the output.
* Added support for `sidebar` elements.
* Solved a bug with `br` elements sometimes adding an unnecessary space.
* Better handling of `tab` elements.
* Merge consecutive span with same attributes.
* This package is now available on [PyPi](https://pypi.org/project/idml2docbook/).

## idml2docbook 1.0.0 (2026-01-22)

This work was extracted from [OutDesign](https://gitlab.com/deborderbollore/outdesign/) to better modularise the project.
For past commit history, refer to this repository.