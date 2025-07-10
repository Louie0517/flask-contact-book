import string, secrets

def secret_key():
    alpha = string.ascii_letters + string.digits
    while True:
        password_key = ''.join(secrets.choice(alpha) for i in range(64))
        if (any(p.lower() for p in password_key) and (p.upper() for p in password_key) 
            and (p.isdigit() for p in password_key ) >= 26):
            break

if __name__ == "__main__":
    secret_key()