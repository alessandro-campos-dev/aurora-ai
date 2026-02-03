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
    embedding_descricao VECTOR(384),
    
    -- Metadados
    canal_entrada VARCHAR(50) CHECK (canal_entrada IN ('app', 'web', 'presencial', 'telemedicina')),
    tempo_triagem_ia INTERVAL,
    modelo_ia_utilizado VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_triagem_data (created_at),
    INDEX idx_triagem_prioridade (prioridade_ia),
    INDEX idx_triagem_unidade (unidade_id)
);

-- Tabela de Filas
CREATE TABLE filas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    triagem_id UUID UNIQUE REFERENCES triagens(id),
    unidade_id UUID REFERENCES unidades_saude(id),
    posicao INT NOT NULL,
    prioridade VARCHAR(20) NOT NULL,
    tempo_estimado_espera INTERVAL,
    tempo_real_espera INTERVAL,
    status VARCHAR(20) DEFAULT 'aguardando' CHECK (status IN ('aguardando', 'em_atendimento', 'finalizado', 'cancelado')),
    entrada_fila TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    saida_fila TIMESTAMP,
    INDEX idx_fila_status (status),
    INDEX idx_fila_unidade_prioridade (unidade_id, prioridade, entrada_fila)
);

-- Tabela de Atendimentos
CREATE TABLE atendimentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fila_id UUID REFERENCES filas(id),
    medico_id UUID,
    especialidade VARCHAR(100),
    diagnostico TEXT,
    procedimentos TEXT[],
    medicamentos_prescritos TEXT[],
    encaminhamento VARCHAR(200),
    tempo_atendimento INTERVAL,
    satisfacao_paciente INT CHECK (satisfacao_paciente BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finalizado_at TIMESTAMP,
    INDEX idx_atendimento_data (created_at),
    INDEX idx_atendimento_medico (medico_id)
);

-- Tabela de Modelos de IA (versionamento)
CREATE TABLE modelos_ia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) NOT NULL,
    versao VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('classificacao', 'nlp', 'regressao', 'cluster')),
    metricas JSONB NOT NULL,
    acuracia DECIMAL(5,4),
    recall_emergencia DECIMAL(5,4),
    precisao DECIMAL(5,4),
    data_treinamento DATE NOT NULL,
    arquivo_modelo VARCHAR(255),
    hiperparametros JSONB,
    status VARCHAR(20) DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo', 'teste')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(nome, versao)
);

-- Tabela de Logs de Decisões da IA (para audit e explainability)
CREATE TABLE logs_decisoes_ia (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    triagem_id UUID REFERENCES triagens(id),
    modelo_id UUID REFERENCES modelos_ia(id),
    input_features JSONB NOT NULL,
    output_predicoes JSONB NOT NULL,
    explicabilidade_shap JSONB,
    tempo_processamento INTERVAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_logs_triagem (triagem_id),
    INDEX idx_logs_data (created_at)
);

-- Tabela de Alertas e Monitoramento
CREATE TABLE alertas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unidade_id UUID REFERENCES unidades_saude(id),
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('capacidade', 'tempo_espera', 'equipamento', 'pessoal', 'sistema')),
    nivel VARCHAR(20) NOT NULL CHECK (nivel IN ('baixo', 'medio', 'alto', 'critico')),
    descricao TEXT NOT NULL,
    valor_atual DECIMAL(10,2),
    valor_limite DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'ativo' CHECK (status IN ('ativo', 'resolvido', 'monitorando')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolvido_at TIMESTAMP,
    INDEX idx_alertas_status (status),
    INDEX idx_alertas_nivel (nivel)
);

-- Tabela de Estatísticas em Tempo Real
CREATE TABLE estatisticas_tempo_real (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unidade_id UUID REFERENCES unidades_saude(id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pacientes_fila INT DEFAULT 0,
    pacientes_atendidos_hora INT DEFAULT 0,
    tempo_medio_espera INTERVAL,
    ocupacao_percentual DECIMAL(5,2),
    taxa_ocupacao_emergencia DECIMAL(5,2),
    taxa_ocupacao_urgente DECIMAL(5,2),
    INDEX idx_estatisticas_timestamp (timestamp),
    INDEX idx_estatisticas_unidade (unidade_id, timestamp)
);

-- Tabela de Telemedicina
CREATE TABLE sessoes_telemedicina (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    paciente_id UUID REFERENCES pacientes(id),
    medico_id UUID,
    sala_webrtc VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'agendada' CHECK (status IN ('agendada', 'em_andamento', 'concluida', 'cancelada')),
    data_agendada TIMESTAMP NOT NULL,
    data_inicio TIMESTAMP,
    data_fim TIMESTAMP,
    duracao INTERVAL,
    gravacao_url VARCHAR(255),
    transcricao_texto TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_telemedicina_status (status),
    INDEX idx_telemedicina_data (data_agendada)
);

-- Views para facilitar consultas

-- View: Dashboard de Monitoramento
CREATE VIEW dashboard_monitoramento AS
SELECT 
    u.nome as unidade,
    u.tipo,
    u.cidade,
    COUNT(DISTINCT f.id) as pacientes_fila,
    COUNT(DISTINCT CASE WHEN f.status = 'em_atendimento' THEN f.id END) as em_atendimento,
    AVG(EXTRACT(EPOCH FROM f.tempo_real_espera)/60) as tempo_medio_espera_min,
    COUNT(DISTINCT t.id) as triagens_24h,
    COUNT(DISTINCT CASE WHEN t.prioridade_ia = 'emergencia' THEN t.id END) as emergencias_24h
FROM unidades_saude u
LEFT JOIN filas f ON f.unidade_id = u.id AND f.status IN ('aguardando', 'em_atendimento')
LEFT JOIN triagens t ON t.unidade_id = u.id AND t.created_at >= NOW() - INTERVAL '24 hours'
GROUP BY u.id, u.nome, u.tipo, u.cidade;

-- View: Performance da IA
CREATE VIEW performance_ia AS
SELECT 
    DATE(t.created_at) as data,
    COUNT(*) as total_triagens,
    SUM(CASE WHEN t.acerto_ia = TRUE THEN 1 ELSE 0 END) as acertos,
    ROUND(100.0 * SUM(CASE WHEN t.acerto_ia = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) as acuracia_dia,
    m.nome as modelo,
    m.versao
FROM triagens t
LEFT JOIN logs_decisoes_ia l ON l.triagem_id = t.id
LEFT JOIN modelos_ia m ON m.id = l.modelo_id
WHERE t.prioridade_medico IS NOT NULL
GROUP BY DATE(t.created_at), m.nome, m.versao
ORDER BY data DESC;

-- Índices para performance
CREATE INDEX idx_triagens_embedding ON triagens USING ivfflat (embedding_sintomas vector_cosine_ops);
CREATE INDEX idx_triagens_similaridade ON triagens USING ivfflat (embedding_descricao vector_cosine_ops);
CREATE INDEX idx_filas_prioridade_entrada ON filas(prioridade, entrada_fila);
CREATE INDEX idx_estatisticas_agregado ON estatisticas_tempo_real(unidade_id, timestamp DESC);

-- Função para atualizar timestamp automático
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_unidades_updated_at BEFORE UPDATE ON unidades_saude
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Função para cálculo de similaridade de sintomas
CREATE OR REPLACE FUNCTION calcular_similaridade_sintomas(
    embedding_input VECTOR(384),
    limite_similaridade DECIMAL DEFAULT 0.7
)
RETURNS TABLE (
    triagem_id UUID,
    sintomas TEXT,
    similaridade DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id,
        t.sintomas,
        1 - (t.embedding_sintomas <=> embedding_input) as similaridade
    FROM triagens t
    WHERE 1 - (t.embedding_sintomas <=> embedding_input) > limite_similaridade
    ORDER BY similaridade DESC
    LIMIT 10;
END;
$$ LANGUAGE plpgsql;

-- Comentários para documentação
COMMENT ON TABLE triagens IS 'Registros de triagem com embeddings para similaridade de casos';
COMMENT ON COLUMN triagens.embedding_sintomas IS 'Embedding vetorial dos sintomas para busca por similaridade';
COMMENT ON COLUMN triagens.score_emergencia IS 'Score de confiança para classificação de emergência (0-1)';
COMMENT ON TABLE modelos_ia IS 'Registro de versionamento dos modelos de IA utilizados';
COMMENT ON TABLE logs_decisoes_ia IS 'Logs completos para audit trail e explicabilidade de decisões da IA';
