
## Medidas Técnicas de Segurança

### Criptografia
```python
# Exemplo de implementação
from cryptography.fernet import Fernet
import base64

class DataEncryptor:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_health_data(self, data: dict) -> str:
        """Criptografa dados sensíveis de saúde"""
        json_str = json.dumps(data)
        encrypted = self.cipher.encrypt(json_str.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_health_data(self, encrypted_data: str) -> dict:
        """Descriptografa dados sensíveis"""
        decoded = base64.b64decode(encrypted_data)
        decrypted = self.cipher.decrypt(decoded)
        return json.loads(decrypted.decode())
