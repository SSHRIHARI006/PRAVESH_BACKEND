from Crypto.Cipher import AES
import base64
import json
import os
from dotenv import load_dotenv

# Same key as Flutter (must be 32 bytes for AES-256)
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')  # 32 bytes
IV = b'\x00' * 16  # 16 bytes of zero like Flutter used

def decrypt_qr_data(encrypted_b64: str) -> dict:
    try:
        encrypted_bytes = base64.b64decode(encrypted_b64)
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
        decrypted = cipher.decrypt(encrypted_bytes)
        # Remove padding (PKCS7)
        pad_len = decrypted[-1]
        decrypted = decrypted[:-pad_len]
        return json.loads(decrypted.decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")
