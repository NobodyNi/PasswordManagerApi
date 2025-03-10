from cryptography.fernet import Fernet


# генерация ключа
def generate_key():
    return Fernet.generate_key()


# шифрование пароля
def encrypt_password(password: str, key: bytes) -> str:
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password.decode()


# дешифрование пароля
def decrypt_password(encrypted_password: str, key: bytes) -> str:
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
    return decrypted_password.decode()
