from dotenv import load_dotenv, dotenv_values
from uuid import uuid4
import platform
import os

from datetime import timedelta

load_dotenv()
values = dotenv_values()

login_db = os.getenv('login')
passwd_db = os.getenv('password')
host_db = os.getenv('host')
database_name = os.getenv('database')


## FLASK-MAIL CONFIG
MAIL_SERVER = values['MAIL_SERVER']
MAIL_PORT = int(values['MAIL_PORT'])
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = values['MAIL_USERNAME']
MAIL_PASSWORD = values['MAIL_PASSWORD']
MAIL_DEFAULT_SENDER = values['MAIL_DEFAULT_SENDER']

## SQLALCHEMY CONFIG
debug = os.getenv('DEBUG', 'False').lower() in (
        'true', '1', 't', 'y', 'yes')

database_uri = f"mysql://{login_db}:{passwd_db}@{host_db}/{database_name}"
if debug is True:
    database_uri = "sqlite:///project.db"

SQLALCHEMY_DATABASE_URI = database_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

## FLASK CONFIG   
PREFERRED_URL_SCHEME = "https"
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = timedelta(days=31).max.seconds
SECRET_KEY = str(uuid4())

## File paths config
PDF_PATH = os.path.join(os.getcwd(), "PDF")
DOCS_PATH = os.path.join(os.getcwd(), "Docs")
TEMP_PATH = os.path.join(os.getcwd(), "Temp")
IMAGE_TEMP_PATH = os.path.join(TEMP_PATH, "IMG")
CSV_TEMP_PATH = os.path.join(TEMP_PATH, "csv")
PDF_TEMP_PATH = os.path.join(TEMP_PATH, "pdf")
SRC_IMG_PATH = os.path.join(os.getcwd(), "app", "src", "assets", "img")

for paths in [DOCS_PATH, TEMP_PATH, IMAGE_TEMP_PATH, CSV_TEMP_PATH, PDF_TEMP_PATH]:
    
    if not os.path.exists(paths):
        os.makedirs(paths, exist_ok=True)
        
    else:
        
        plataforma = platform.system()
        
        if plataforma == "Linux":
            path =  f"{paths}" 
            command = "rm -r " + path
             
        
        elif plataforma == "Windows":
            path =  f"{paths}\\*" 
            command = "powershell rm -r " + path
        
        os.system(command)


