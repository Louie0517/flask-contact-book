import string, secrets, os

def secret_k():
    p_len = 64
    alpha = string.ascii_letters + string.digits + string.punctuation
    while True:
        password_key = ''.join(secrets.choice(alpha) for _ in range(p_len))
        if (any(p.lower() for p in password_key) and 
            any(p.upper() for p in password_key) and 
            sum(p.isdigit() for p in password_key ) >= 26):
    
        
            password_key = os.getenv('SECRET_KEY')
            
            return password_key

if __name__ == "__main__":
    secret_k()