from cryptography.fernet import Fernet

def encrypt(filename):
    with open("key.key","rb") as rb:
        key = rb.read()
    with open(filename,"rb") as rb:
        data = rb.read()
    encrypter = Fernet(key)
    encrypted = encrypter.encrypt(data)
    with open(filename,"wb") as wb:
        wb.write(encrypted)

def decrypt(filename):
    with open("key.key","rb") as rb:
        key = rb.read()
    with open(filename,"rb") as rb:
        data = rb.read()
    decrypter = Fernet(key)
    decrypted = decrypter.decrypt(data)
    with open(filename,"wb") as wb:
        wb.write(decrypted)