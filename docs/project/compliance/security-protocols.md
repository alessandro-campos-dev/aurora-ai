
#### **Arquivo 26: docs/project/compliance/security-protocols.md**
```markdown
# Protocolos de Segurança - Aurora AI

## Visão Geral

Este documento estabelece os protocolos de segurança implementados no Aurora AI para proteção de dados, sistemas e infraestrutura. Baseado em frameworks reconhecidos (NIST, ISO 27001) e adaptado aos requisitos específicos de saúde digital.

## Política de Segurança da Informação

### Princípios Fundamentais
1. **Confidencialidade**: Dados acessíveis apenas a autorizados
2. **Integridade**: Dados precisos e completos
3. **Disponibilidade**: Acesso quando necessário
4. **Rastreabilidade**: Todas as ações registradas
5. **Conformidade**: Alinhamento com LGPD, ANVISA, HIPAA

### Abrangência
- Todos os sistemas Aurora AI
- Equipe e colaboradores
- Parceiros e fornecedores
- Dados em trânsito e repouso

## Controles de Acesso

### Autenticação
```python
# Exemplo: Implementação JWT com claims específicas
from jose import JWTError, jwt
from datetime import datetime, timedelta

class AuthService:
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "iss": "aurora-ai",
            "aud": "aurora-ai-users",
            # Claims específicas para saúde
            "role": data.get("role"),
            "permissions": self._get_role_permissions(data["role"]),
            "facility_id": data.get("facility_id"),  # Limitação de escopo
            "mfa_verified": data.get("mfa_enabled", False)
        })
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.secret_key, 
            algorithm=self.algorithm
        )
        return encoded_jwt
    
    def _get_role_permissions(self, role: str) -> list:
        """Define permissões baseadas em papel"""
        permissions = {
            "patient": ["read_own_data", "create_triage"],
            "doctor": ["read_patient_data", "validate_triage", "prescribe"],
            "admin": ["*"],
            "auditor": ["read_all", "export_reports"]
        }
        return permissions.get(role, [])
