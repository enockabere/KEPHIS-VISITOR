from cryptography.fernet import Fernet

def Encrypt():
    """_summary_ FnVisitorsCard and field where that service appears
    
    LPO/LSO  = 1
    Cheque = 2
    Mpesa = 3

    """
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(b"1234567")
    print(key)
Encrypt()


