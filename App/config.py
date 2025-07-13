from dotenv import load_dotenv
import os

class Config:
    
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECRET_EMAIL = os.getenv('ADMIN_EMAIL')
    SECRET_PASSWORD = os.getenv('ADMIN_PASSWORD')
    
def get_v():
    cf : Config = Config()
    return cf.SECRET_EMAIL, cf.SECRET_PASSWORD
