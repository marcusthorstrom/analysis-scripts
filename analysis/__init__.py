import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

current_dir = Path(__file__).parent.absolute()
project_dir = current_dir / '..'
env_path = current_dir / '..' / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

READ_TOKEN = os.getenv("READ_TOKEN")
READ_API_URL = os.getenv("READ_API_URL")

DATABASE = 'covid_dev'

INPUT_DATASETS_PATH = project_dir/ 'input_datasets'
OUTPUT_DATASETS_PATH = project_dir / 'output_datasets'
BACKUP_PATH = project_dir / 'backups'
BACKUP_DOCUMENTS_PATH = BACKUP_PATH / 'documents'

# input for gps coordinates
GEO_DATA_FILE_FIRST = INPUT_DATASETS_PATH / 'geocoding.csv'
GEO_DATA_FILE_SECOND = INPUT_DATASETS_PATH / 'plz_text.csv'

# outputs
DAILY_REPORT_DIR = OUTPUT_DATASETS_PATH / 'daily-reports'
GEO_LOCATION_DIR = OUTPUT_DATASETS_PATH / 'geo-locations'
OUTPUT_GEO_CODING_FILE = GEO_LOCATION_DIR / 'geocoding.csv'

if not OUTPUT_DATASETS_PATH.exists():
    OUTPUT_DATASETS_PATH.mkdir()

if not BACKUP_PATH.exists():
    BACKUP_PATH.mkdir()

if not BACKUP_DOCUMENTS_PATH.exists():
    BACKUP_DOCUMENTS_PATH.mkdir()

if not DAILY_REPORT_DIR.exists():
    DAILY_REPORT_DIR.mkdir()

if not GEO_LOCATION_DIR.exists():
    GEO_LOCATION_DIR.mkdir()
