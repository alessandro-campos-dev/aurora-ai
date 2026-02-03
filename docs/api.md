# 📡 Documentação da API Aurora AI

## Visão Geral

A API do Aurora AI fornece endpoints RESTful e WebSocket para integração com o sistema de gestão hospitalar inteligente. Todas as respostas são em formato JSON.

**URL Base**: `https://api.aurora-ai.health/v1`

## Autenticação

### Método: JWT Bearer Token

```http
Authorization: Bearer <seu_jwt_token>
