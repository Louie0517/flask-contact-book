import string, secrets


def secret_k(len=64):
    alpha = string.ascii_letters + string.digits
    while True:
        password_key = ''.join(secrets.choice(alpha) for _ in range(len))
        if (any(p.lower() for p in password_key) and 
            any(p.upper() for p in password_key) and 
            sum(p.isdigit() for p in password_key ) >= 26):
            
            return password_key

if __name__ == "__main__":
    secret_k()