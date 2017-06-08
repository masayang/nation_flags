from os.path import join, dirname
from dotenv import load_dotenv
import os, json


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

config = {
    'ENGLISH_URL': os.environ.get("ENGLISH_URL"),
    'JAPANESE_URL': os.environ.get("JAPANESE_URL"),
    'WIKIPEDIA_BASE_URL': os.environ.get("WIKIPEDIA_BASE_URL"),
    'WIKIPEDIA_BASE_URL_J': os.environ.get("WIKIPEDIA_BASE_URL_J")
}


if __name__ == '__main__':
    print(json.dumps(config, indent=4, sort_keys=True))