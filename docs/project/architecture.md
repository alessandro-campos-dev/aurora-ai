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
