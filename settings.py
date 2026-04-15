import configparser
import os

# Creamos el lector de configuración
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

# Definimos constantes globales para usar en todo el proyecto
VERSION = config.get('APP', 'version')
AUTHOR = config.get('APP', 'author')
EMAIL = config.get('APP', 'email')

URL_SIU = config.get('NETWORK', 'url_siu')

TMP_DIR = config.get('PATHS', 'tmp_dir')
LOGO_PATH = config.get('PATHS', 'logo_gobierno')
FAVICON_PATH = config.get('PATHS', 'favicon')

PDF_DEFAULT_NAME = config.get('PDF', 'default_filename')