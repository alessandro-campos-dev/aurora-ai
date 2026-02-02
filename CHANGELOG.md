# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-15

### Adicionado
- Estrutura inicial do projeto
- Configuração Docker e docker-compose
- API FastAPI básica com endpoints de triagem
- Frontend React com Vite
- Dashboard Streamlit de demonstração
- Pipeline CI/CD com GitHub Actions
- Documentação completa
- Modelos de ML básicos para classificação
- Sistema de autenticação JWT
- Banco de dados PostgreSQL com migrações
- Cache Redis para performance
- Testes unitários e de integração
- Pre-commit hooks para qualidade de código
- Configuração de monitoramento básica
- Estrutura de pastas para escalabilidade

### Alterado
- Nenhuma alteração ainda

### Corrigido
- Nenhuma correção ainda

### Segurança
- Implementação inicial de segurança com JWT
- Configuração de CORS
- Validação de entrada de dados
- Proteção contra SQL injection
- Logging seguro sem dados sensíveis

## [Planejado para 0.2.0]

### Adicionado
- Integração com sistemas de saúde reais
- Modelos de ML mais avançados
- Sistema de notificações por SMS/Email
- Dashboard administrativo completo
- Relatórios analíticos
- Suporte a múltiplos idiomas
- APIs para telemedicina
- Sistema de agendamento inteligente
- Módulo de prescrição digital

### Melhorado
- Performance de inferência de ML
- Experiência do usuário mobile
- Documentação da API
- Testes de carga e performance
- Monitoramento e alertas
- Processo de deploy

### Alterado
- Estrutura de banco para suportar mais funcionalidades
- Arquitetura para microserviços

### Corrigido
- Problemas de performance conhecidos
- Bugs de interface identificados
- Vulnerabilidades de segurança

---

## Guia de Versionamento

- **MAJOR version**: Mudanças incompatíveis na API
- **MINOR version**: Nova funcionalidade compatível
- **PATCH version**: Correções de bugs compatíveis
