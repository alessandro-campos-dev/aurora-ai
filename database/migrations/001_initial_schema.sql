-- Migration: 001_initial_schema.sql
-- Data: 2024-01-01
-- Autor: Sistema Aurora AI
-- Descrição: Schema inicial do banco de dados

BEGIN;

-- Executar o schema completo
\i ../schema.sql

-- Inserir dados iniciais
INSERT INTO unidades_saude (nome, tipo, endereco, cidade, estado, capacidade) VALUES
('UPA Centro', 'UPA', 'Rua Principal, 123', 'São Paulo', 'SP', 150),
('Hospital Municipal', 'Hospital', 'Av. Saúde, 456', 'São Paulo', 'SP', 300),
('UBS Jardim Saúde', 'UBS', 'Rua das Flores, 789', 'São Paulo', 'SP', 80);

COMMIT;
