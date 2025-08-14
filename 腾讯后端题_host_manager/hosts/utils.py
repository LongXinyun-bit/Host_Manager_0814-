import base64
import os
from cryptography.fernet import Fernet
from django.conf import settings


# 为了示例简化：从 SECRET_KEY 派生一个稳定 key，用于本地加密。生产中请改为 KMS/HSM。
_derived_key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode('utf-8')[:32].ljust(32, b'0'))
_cipher = Fernet(_derived_key)


def encrypt_text(plain_text: str) -> str:
    token = _cipher.encrypt(plain_text.encode('utf-8'))
    return token.decode('utf-8')


def decrypt_text(token_text: str) -> str:
    data = _cipher.decrypt(token_text.encode('utf-8'))
    return data.decode('utf-8')


def generate_random_password(length: int = 16) -> str:
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-='
    return ''.join(alphabet[c % len(alphabet)] for c in os.urandom(length)) 