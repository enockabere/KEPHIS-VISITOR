from cryptography.fernet import Fernet

def Encrypt():
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(b"1234567")
    print(key)
Encrypt()


