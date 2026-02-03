#!/usr/bin/env python3
"""
Configuração do PostgreSQL com extensão pgvector para embeddings.
Este script configura o banco de dados para armazenar embeddings vetoriais.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
import sys
from typing import Optional
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VectorDatabaseSetup:
    """Classe para configuração do banco de dados vetorial."""
    
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 5432,
                 database: str = "aurora_ai",
                 user: str = "admin",
                 password: str = "aurora123"):
        
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        
        self.connection_params = {
            'host': host,
            'port': port,
            'user': user,
            'password': password
        }
    
    def test_connection(self) -> bool:
        """Testa a conexão com o PostgreSQL."""
        try:
            conn = psycopg2.connect(**self.connection_params, database='postgres')
            conn.close()
            logger.info("✅ Conexão com PostgreSQL estabelecida")
            return True
        except Exception as e:
            logger.error(f"❌ Falha na conexão: {e}")
            return False
    
    def create_database(self) -> bool:
        """Cria o banco de dados se não existir."""
        try:
            # Conecta ao banco de template
            conn = psycopg2.connect(**self.connection_params, database='postgres')
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Verifica se o banco já existe
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.database,))
            exists = cursor.fetchone()
            
            if not exists:
                cursor.execute(f'CREATE DATABASE {self.database}')
                logger.info(f"✅ Banco de dados '{self.database}' criado")
            else:
                logger.info(f"📁 Banco de dados '{self.database}' já existe")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar banco de dados: {e}")
            return False
    
    def enable_vector_extension(self) -> bool:
        """Habilita a extensão pgvector no banco de dados."""
        try:
            conn = psycopg2.connect(**self.connection_params, database=self.database)
            cursor = conn.cursor()
            
            # Habilita a extensão pgvector
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            conn.commit()
            
            # Verifica se a extensão foi habilitada
            cursor.execute("""
                SELECT extname, extversion 
                FROM pg_extension 
                WHERE extname = 'vector'
            """)
            
            result = cursor.fetchone()
            if result:
                logger.info(f"✅ Extensão pgvector habilitada (versão: {result[1]})")
            else:
                logger.warning("⚠️ Extensão pgvector não encontrada após criação")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao habilitar extensão vector: {e}")
            return False
    
    def create_vector_tables(self) -> bool:
        """Cria tabelas específicas para armazenamento vetorial."""
        try:
            conn = psycopg2.connect(**self.connection_params, database=self.database)
            cursor = conn.cursor()
            
            # Tabela de embeddings de sintomas para busca semântica
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS embeddings_sintomas (
                    id SERIAL PRIMARY KEY,
                    sintoma VARCHAR(255) NOT NULL,
                    embedding VECTOR(384) NOT NULL,
                    categoria VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    -- Índice para busca por similaridade
                    CONSTRAINT embedding_unique UNIQUE(sintoma)
                );
            """)
            
            # Índice para busca por similaridade (IVFFlat para produção)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_embeddings_sintomas 
                ON embeddings_sintomas 
                USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100);
            """)
            
            # Tabela de cache de embeddings (para otimização)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cache_embeddings (
                    texto_hash VARCHAR(64) PRIMARY KEY,
                    texto_original TEXT NOT NULL,
                    embedding VECTOR(384) NOT NULL,
                    modelo_utilizado VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            conn.commit()
            logger.info("✅ Tabelas vetoriais criadas com sucesso")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar tabelas vetoriais: {e}")
            return False
    
    def populate_initial_embeddings(self) -> bool:
        """Popula embeddings iniciais de sintomas comuns."""
        try:
            # Sintomas comuns e seus embeddings de exemplo
            # Nota: Em produção, esses embeddings seriam gerados pelo modelo BERT
            sintomas_comuns = [
                ("febre", "sintoma_geral"),
                ("tosse", "respiratorio"),
                ("dor de cabeça", "neurologico"),
                ("falta de ar", "respiratorio"),
                ("dor no peito", "cardiologico"),
                ("dor abdominal", "gastrointestinal"),
                ("nausea", "gastrointestinal"),
                ("tontura", "neurologico"),
                ("sangramento", "circulatorio"),
                ("inchaço", "circulatorio")
            ]
            
            conn = psycopg2.connect(**self.connection_params, database=self.database)
            cursor = conn.cursor()
            
            for sintoma, categoria in sintomas_comuns:
                # Gera um embedding fictício (384 dimensões)
                # Em produção, substituir pela chamada real ao modelo BERT
                embedding_ficticio = [0.1] * 384  # Embedding de exemplo
                
                cursor.execute("""
                    INSERT INTO embeddings_sintomas (sintoma, embedding, categoria)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (sintoma) DO UPDATE SET
                        embedding = EXCLUDED.embedding,
                        categoria = EXCLUDED.categoria;
                """, (sintoma, embedding_ficticio, categoria))
            
            conn.commit()
            logger.info(f"✅ {len(sintomas_comuns)} embeddings iniciais populados")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao popular embeddings iniciais: {e}")
            return False
    
    def test_vector_operations(self) -> bool:
        """Testa operações vetoriais básicas."""
        try:
            conn = psycopg2.connect(**self.connection_params, database=self.database)
            cursor = conn.cursor()
            
            # Testa similaridade de cosseno
            test_embedding = [0.1] * 384
            
            cursor.execute("""
                SELECT 
                    sintoma,
                    1 - (embedding <=> %s::vector) as similaridade
                FROM embeddings_sintomas
                ORDER BY similaridade DESC
                LIMIT 3;
            """, (test_embedding,))
            
            resultados = cursor.fetchall()
            logger.info("🧪 Teste de similaridade vetorial:")
            for sintoma, similaridade in resultados:
                logger.info(f"   - {sintoma}: {similaridade:.4f}")
            
            # Testa operações matemáticas vetoriais
            cursor.execute("SELECT embedding + embedding FROM embeddings_sintomas LIMIT 1;")
            logger.info("✅ Operações vetoriais funcionando corretamente")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao testar operações vetoriais: {e}")
            return False
    
    def create_hybrid_search_function(self) -> bool:
        """Cria função para busca híbrida (texto + vetorial)."""
        try:
            conn = psycopg2.connect(**self.connection_params, database=self.database)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE OR REPLACE FUNCTION buscar_sintomas_similares(
                    query_text TEXT,
                    query_embedding VECTOR(384),
                    limite_similaridade DECIMAL DEFAULT 0.5,
                    limite_resultados INT DEFAULT 10
                )
                RETURNS TABLE (
                    sintoma VARCHAR,
                    categoria VARCHAR,
                    similaridade_vetorial DECIMAL,
                    similaridade_textual DECIMAL,
                    score_final DECIMAL
                ) AS $$
                BEGIN
                    RETURN QUERY
                    SELECT 
                        es.sintoma,
                        es.categoria,
                        -- Similaridade vetorial (cosseno)
                        1 - (es.embedding <=> query_embedding) as sim_vetorial,
                        -- Similaridade textual (trigram)
                        similarity(es.sintoma, query_text) as sim_textual,
                        -- Score combinado (70% vetorial, 30% textual)
                        (0.7 * (1 - (es.embedding <=> query_embedding)) + 
                         0.3 * similarity(es.sintoma, query_text)) as score_final
                    FROM embeddings_sintomas es
                    WHERE 
                        -- Filtro por similaridade vetorial
                        1 - (es.embedding <=> query_embedding) > limite_similaridade OR
                        -- OU filtro por similaridade textual
                        similarity(es.sintoma, query_text) > 0.3
                    ORDER BY score_final DESC
                    LIMIT limite_resultados;
                END;
                $$ LANGUAGE plpgsql;
            """)
            
            conn.commit()
            logger.info("✅ Função de busca híbrida criada")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar função de busca híbrida: {e}")
            return False
    
    def run_full_setup(self) -> bool:
        """Executa o setup completo do banco de dados vetorial."""
        logger.info("🚀 Iniciando setup do banco de dados vetorial...")
        
        steps = [
            ("Teste de conexão", self.test_connection),
            ("Criação do banco de dados", self.create_database),
            ("Habilitação da extensão vector", self.enable_vector_extension),
            ("Criação de tabelas vetoriais", self.create_vector_tables),
            ("População de embeddings iniciais", self.populate_initial_embeddings),
            ("Criação de função de busca híbrida", self.create_hybrid_search_function),
            ("Teste de operações vetoriais", self.test_vector_operations)
        ]
        
        success = True
        for step_name, step_func in steps:
            logger.info(f"\n🔧 {step_name}...")
            if not step_func():
                logger.error(f"❌ Falha em: {step_name}")
                success = False
                break
        
        if success:
            logger.info("\n🎉 Setup do banco de dados vetorial concluído com sucesso!")
            logger.info(f"📊 Banco: {self.database}")
            logger.info(f"📍 Host: {self.host}:{self.port}")
            logger.info(f"👤 Usuário: {self.user}")
            logger.info("\n✨ Recursos disponíveis:")
            logger.info("   • Extensão pgvector habilitada")
            logger.info("   • Tabelas para embeddings")
            logger.info("   • Índices IVFFlat para busca eficiente")
            logger.info("   • Funções de busca híbrida")
            logger.info("   • Cache de embeddings")
        else:
            logger.error("\n💥 Setup falhou. Verifique os logs acima.")
        
        return success


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup do banco de dados vetorial Aurora AI')
    parser.add_argument('--host', default='localhost', help='Host do PostgreSQL')
    parser.add_argument('--port', type=int, default=5432, help='Porta do PostgreSQL')
    parser.add_argument('--database', default='aurora_ai', help='Nome do banco de dados')
    parser.add_argument('--user', default='admin', help='Usuário do banco')
    parser.add_argument('--password', default='aurora123', help='Senha do banco')
    
    args = parser.parse_args()
    
    # Cria instância do setup
    setup = VectorDatabaseSetup(
        host=args.host,
        port=args.port,
        database=args.database,
        user=args.user,
        password=args.password
    )
    
    # Executa setup completo
    success = setup.run_full_setup()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
