import os
import sys
import logging
import contextlib
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

VERSION = __version__ = "1.1.3"

LOGGER = logging.basicConfig(filename='idml2docbook.log', encoding='utf-8', level=logging.DEBUG)

load_dotenv()

def getEnvOrDefault(envConst, default=False):
    return os.getenv(envConst) if os.getenv(envConst) else default

IDML2HUBXML_SCRIPT_FOLDER = os.getenv("IDML2HUBXML_SCRIPT_FOLDER")

DEFAULT_OPTIONS = {
    'idml2hubxml_file': False,
    'typography': getEnvOrDefault("TYPOGRAPHY"),
    'ignore_overrides': getEnvOrDefault("IGNORE_OVERRIDES"),
    'thin_spaces': getEnvOrDefault("THIN_SPACES"),
    'linebreaks': getEnvOrDefault("LINEBREAKS"),
    'media': getEnvOrDefault("MEDIA", "Links"),
    'raster': getEnvOrDefault("RASTER", None),
    'vector': getEnvOrDefault("VECTOR", None),
    'idml2hubxml_output': getEnvOrDefault("IDML2HUBXML_OUTPUT_FOLDER", "idml2hubxml"),
    'idml2hubxml_script': IDML2HUBXML_SCRIPT_FOLDER,
}