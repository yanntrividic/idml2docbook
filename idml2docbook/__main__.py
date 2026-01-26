"""Command-line interface to idml2docbook."""

import argparse
import logging
import os

from . import __version__, LOGGER, DEFAULT_OPTIONS
from .core import idml2docbook

# This file structure is inspired from weasyprint:
# https://github.com/Kozea/WeasyPrint/blob/main/weasyprint/__main__.py
class Parser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        self._arguments = {}
        super().__init__(*args, **kwargs)

    # def add_argument(self, *args, **kwargs):
    #     super().add_argument(*args, **kwargs)
    #     key = args[-1].lstrip('-')
    #     kwargs['flags'] = args
    #     kwargs['positional'] = args[-1][0] != '-'
    #     self._arguments[key] = kwargs

    @property
    def docstring(self):
        self._arguments['help'] = self._arguments.pop('help')
        data = []
        for key, args in self._arguments.items():
            data.append('.. option:: ')
            action = args.get('action', 'store')
            for flag in args['flags']:
                data.append(flag)
                if not args['positional'] and action in ('store', 'append'):
                    data.append(f' <{key}>')
                data.append(', ')
            data[-1] = '\n\n'
            data.append(f'  {args["help"][0].upper()}{args["help"][1:]}.\n\n')
        return ''.join(data)

def load_env(argv):

    PARSER = Parser(
        prog='idml2docbook',
        description='Convert IDML files to DocBook.',
        usage='%(prog)s [options]')
    PARSER.add_argument(
        'input', help='filename of the IDML input')
    PARSER.add_argument(
        '-x', '--idml2hubxml-file', action='store_true',
        help='consider this file as a hubxml file, '
        'this can be handy to gain computing time if you '
        'have already performed idml2xml on your IDML source file')
    PARSER.add_argument(
        '-o', '--output', type=str,
        help='filename where output is written, defaults to stdout')
    PARSER.add_argument(
        '-g', '--ignore-overrides', action='store_true',
        help='ignore the style overrides (direct formatting)')
    PARSER.add_argument(
        '-t', '--typography', action='store_true',
        help='redo the orthotypography '
        '(french typography rules, with thin spaces, nbsp...)')
    PARSER.add_argument(
        '-l', '--thin-spaces', action='store_true',
        help='only use thin spaces in the refactoring of the '
        'orthotography, works in pair with --typography')
    PARSER.add_argument(
        '-b', '--linebreaks', action='store_true',
        help='do not replace <br> tags with spaces')
    PARSER.add_argument(
        '-f', '--media', type=str,
        help='path to the media folder, defaults to "Links"')
    PARSER.add_argument(
        '-r', '--raster', type=str,
        help='extension to replace raster media files extensions with, '
        'e.g. "jpg", defaults to None')
    PARSER.add_argument(
        '-v', '--vector', type=str,
        help='extension to replace vector media files extensions with, '
        'e.g. "svg", defaults to None')
    PARSER.add_argument(
        '-i', '--idml2hubxml-output', type=str,
        help='path to the output of Transpect’s idml2hubxml converter, '
        'defaults to "idml2hubxml"')
    PARSER.add_argument(
        '-s', '--idml2hubxml-script', type=str,
        help='path to the script of Transpect’s idml2xml converter, '
        'defaults to "idml2xml-frontend"')
    PARSER.add_argument(
        '--version', action='version',
        version=f'idml2docbook version {__version__}',
        help='print idml2docbook’s version number and exit')

    args = PARSER.parse_args(argv)

    default_options = DEFAULT_OPTIONS

    PARSER.set_defaults(**default_options)

    logging.debug("Parsed command-line arguments: " + str(args))
    return PARSER.parse_args(argv), default_options

def main(argv=None, stdout=None, stdin=None):

    args, default_options = load_env(argv)

    options = {
        key: value for key, value in vars(args).items() if key in default_options
    }

    if not options["idml2hubxml_script"]:
        raise RuntimeError(
            "Missing IDML2HUBXML_SCRIPT_FOLDER in .env file.\n"
            "You might want to edit your .env file or run the following command\n"
            "to check your configuration and install missing external dependencies:\n\n"
            "idml2docbook-install-dependencies"
        )

    docbook = idml2docbook(args.input, **options)

    if(args.output):
        logging.info("Writing file: " + args.output)
        with open(args.output, "w") as file:
            file.write(docbook)
    else: print(docbook)

if __name__ == "__main__":
    main()