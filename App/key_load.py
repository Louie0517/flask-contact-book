from key import secret_k
import os

def s_k():
    os.environ['APP_KEY'] = secret_k()