-- Aurora AI - Schema do Banco de Dados
-- PostgreSQL com extensão pgvector

-- Extensão para embeddings vetoriais
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabela de Unidades de Saúde
CREATE TABLE unidades_saude (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('UPA', 'Hospital', 'UBS', 'Clinica')),
    endereco TEXT NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    capacidade INT NOT NULL DEFAULT 100,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Pacientes (dados anonimizados)
CREATE TABLE pacientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_anonimo VARCHAR(50) UNIQUE NOT NULL,
    idade INT NOT NULL,
    genero VARCHAR(20),
    comorbidades TEXT[], -- Array de comorbidades
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_paciente_codigo (codigo_anonimo)
);

-- Tabela de Triagens
CREATE TABLE triagens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID REFERENCES pacientes(id) ON DELETE CASCADE,
    unidade_id UUID REFERENCES unidades_saude(id),
    sintomas TEXT NOT NULL,
    descricao_completa TEXT,
    intensidade_dor INT CHECK (intensidade_dor BETWEEN 0 AND 10),
    temperatura DECIMAL(4,2),
    pressao_arterial VARCHAR(20),
    frequencia_cardiaca INT,
    saturacao_o2 DECIMAL(4,2),
    
    -- Classificação da IA
    prioridade_ia VARCHAR(20) CHECK (prioridade_ia IN ('emergencia', 'urgente', 'prioritario', 'eletivo')),
    score_emergencia DECIMAL(5,4),
    score_urgente DECIMAL(5,4),
    score_prioritario DECIMAL(5,4),
    score_eletivo DECIMAL(5,4),
    
    -- Classificação do médico (ground truth)
    prioridade_medico VARCHAR(20),
    acerto_ia BOOLEAN,
    
    -- Embeddings vetoriais para similaridade
    embedding_sintomas VECTOR(384), -- Dimensão do modelo BERT
    embedding_descric
