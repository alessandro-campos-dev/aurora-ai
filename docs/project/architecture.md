# Arquitetura do Sistema Aurora AI

## Visão Geral

Aurora AI é uma aplicação distribuída construída com uma arquitetura baseada em microsserviços. O sistema é projetado para ser escalável, resiliente e seguro, atendendo aos requisitos rigorosos de sistemas de saúde.

## Diagrama de Arquitetura
┌─────────────────────────────────────────────────────────────────────┐
│ Cliente (Browser/Mobile) │
└───────────────────────────────┬─────────────────────────────────────┘
│ HTTPS
┌───────────────────────────────▼─────────────────────────────────────┐
│ Load Balancer (Nginx) │
└─────────────┬─────────────────┬─────────────────┬───────────────────┘
│ │ │
┌─────────▼─────┐ ┌─────────▼─────┐ ┌─────────▼─────┐
│ Frontend │ │ API │ │ Streamlit │
│ (React) │ │ (FastAPI) │ │ (Dashboard) │
└───────┬───────┘ └───────┬───────┘ └───────┬───────┘
│ │ │
┌───────▼─────────────────▼─────────────────▼───────┐
│ Service Mesh │
│ (Autenticação, Logging) │
└───────────────────────┬───────────────────────────┘
│
┌───────────────────────▼───────────────────────────┐
│ Message Broker (Redis) │
└───────────────┬─────────────────┬─────────────────┘
│ │
┌───────────▼─────┐ ┌─────────▼─────┐
│ Workers │ │ Cache │
│ (Celery) │ │ │
└───────────┬─────┘ └───────────────┘
│
┌───────────▼──────────────────────────────────┐
│ Banco de Dados │
│ (PostgreSQL + Vector DB) │
└──────────────────────────────────────────────┘

text

## Componentes Principais

### 1. Frontend (React + TypeScript)
- **Tecnologia**: React 18, TypeScript, Vite
- **Estado**: Zustand para gerenciamento de estado
- **Estilo**: Tailwind CSS
- **Funcionalidades**:
  - Interface de triagem em tempo real
  - Dashboard administrativo
  - Visualização de métricas
  - Sistema de notificações

### 2. API Backend (FastAPI)
- **Tecnologia**: Python 3.10+, FastAPI
- **Banco de Dados**: PostgreSQL com SQLAlchemy
- **Cache**: Redis para sessões e cache
- **Autenticação**: JWT com refresh tokens
- **Documentação**: OpenAPI/Swagger automática

### 3. Serviço de Machine Learning
- **Tecnologia**: Python, Scikit-learn, Transformers
- **Modelos**:
  - Classificação de risco (Random Forest/XGBoost)
  - NLP para extração de sintomas (BERT)
  - Otimização de filas (algoritmos personalizados)
- **Inferência**: FastAPI separado para escalabilidade

### 4. Dashboard (Streamlit)
- **Propósito**: Demonstração e prototipagem rápida
- **Funcionalidades**:
  - Simulação de triagem
  - Visualização de dados
  - Teste de algoritmos

### 5. Infraestrutura
- **Containerização**: Docker + Docker Compose
- **Orquestração**: Kubernetes (produção)
- **Monitoramento**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **CI/CD**: GitHub Actions

## Fluxo de Dados

### Triagem de Paciente
1. **Entrada**: Usuário descreve sintomas via chat
2. **Processamento NLP**: Extração de entidades médicas
3. **Classificação**: Modelo ML classifica risco (baixo/médio/alto/crítico)
4. **Otimização**: Algoritmo sugere melhor unidade de saúde
5. **Saída**: Recomendação + agendamento (se necessário)

### Gestão de Filas
1. **Coleta**: Dados de ocupação em tempo real
2. **Análise**: Previsão de demanda usando séries temporais
3. **Otimização**: Alocação dinâmica de recursos
4. **Atualização**: Interface em tempo real para gestores

## Considerações de Segurança

### Camadas de Segurança
1. **Rede**: VPC isolada, Security Groups
2. **Aplicação**: Rate limiting, input validation
3. **Autenticação**: JWT com expiração curta
4. **Dados**: Criptografia em trânsito e repouso
5. **Compliance**: LGPD, HIPAA (futuro)

### Proteção de Dados Sensíveis
- Anonimização de dados de treinamento
- Logs sem informações pessoais
- Acesso baseado em roles (RBAC)
- Auditoria de todas as operações

## Escalabilidade

### Horizontal Scaling
- API: Stateless, múltiplas instâncias
- ML Service: Auto-scaling baseado em carga
- Banco de Dados: Read replicas, sharding

### Caching Strategy
- Redis para sessões e cache de consultas
- CDN para assets estáticos
- Cache em múltiplos níveis

## Monitoramento e Observabilidade

### Métricas Coletadas
- Tempo de resposta da API
- Taxa de erro por endpoint
- Utilização de recursos
- Performance de modelos ML
- Métricas de negócio (tempos de espera, etc.)

### Alertas Configurados
- Disponibilidade do serviço
- Performance degradada
- Erros aumentando
- Utilização de recursos crítica

## Decisões Arquiteturais

### Por que FastAPI?
- Performance comparável a Go/Node.js
- Type hints integrados
- Geração automática de documentação
- Suporte nativo a async/await

### Por que React?
- Ecossistema maduro
- Server-side rendering possível
- Boa performance para aplicações complexas
- Grande comunidade e recursos

### Por que PostgreSQL?
- ACID compliance
- JSONB para dados semi-estruturados
- Extensões para full-text search
- Vector similarity (pgvector)

### Por que Kubernetes?
- Auto-healing
- Auto-scaling
- Gestão simplificada de múltiplos ambientes
- Portabilidade entre clouds

## Próximos Passos Arquiteturais

### Fase 2 (6 meses)
- Migração para microsserviços completos
- Implementação de event sourcing
- Data lake para analytics
- Multi-region deployment

### Fase 3 (12 meses)
- Edge computing para baixa latência
- Federated learning para privacidade
- Blockchain para auditoria imutável
- Integração com IoT devices

## Diagramas Técnicos Adicionais

### Sequência de Triagem
```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend
    participant A as API
    participant M as ML Service
    participant DB as Database
    
    U->>F: Descreve sintomas
    F->>A: POST /triage
    A->>M: Classifica risco
    M-->>A: Risco + Recomendação
    A->>DB: Salva histórico
    A-->>F: Resposta completa
    F-->>U: Mostra resultado
