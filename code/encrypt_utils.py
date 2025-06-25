
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key().decode()

def encrypt_file(key_str, plaintext_path, cipher_path):
    f = Fernet(key_str.encode())
    with open(plaintext_path,'rb') as infile:
        data=infile.read()
    enc=f.encrypt(data)
    with open(cipher_path,'wb') as outfile:
        outfile.write(enc)

def decrypt_file(key_str, cipher_path):
    f=Fernet(key_str.encode())
    with open(cipher_path,'rb') as infile:
        return f.decrypt(infile.read())
