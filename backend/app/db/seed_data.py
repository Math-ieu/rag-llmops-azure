import json
import uuid
import random
import datetime
import logging
from sqlalchemy import create_engine, text
from app.config import settings
from app.generation.prompts import PROMPT_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """Initialise PostgreSQL avec un ensemble riche de chunks vectoriels, documents et métriques de requêtes."""
    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    logger.info(f"Connexion à la base de données: {db_url.split('@')[-1] if '@' in db_url else db_url}")
    engine = create_engine(db_url, pool_pre_ping=True)

    with engine.begin() as conn:
        # 1. Vérification des extensions & tables
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id VARCHAR(128) PRIMARY KEY,
                content TEXT NOT NULL,
                metadata JSONB NOT NULL,
                embedding vector({settings.VECTOR_DIMENSION}) NOT NULL
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS indexed_documents (
                id VARCHAR(128) PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                file_type VARCHAR(32) NOT NULL DEFAULT 'text',
                chunks_count INT NOT NULL DEFAULT 0,
                file_size_bytes BIGINT DEFAULT 0,
                status VARCHAR(32) NOT NULL DEFAULT 'indexed',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chat_conversations (
                id VARCHAR(128) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                user_id VARCHAR(128) NOT NULL DEFAULT 'default_user',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id VARCHAR(128) PRIMARY KEY,
                conversation_id VARCHAR(128) NOT NULL REFERENCES chat_conversations(id) ON DELETE CASCADE,
                role VARCHAR(32) NOT NULL,
                content TEXT NOT NULL,
                timestamp_str VARCHAR(64),
                trace_id VARCHAR(128),
                sources JSONB DEFAULT '[]'::jsonb,
                metrics JSONB DEFAULT '{}'::jsonb,
                feedback_given SMALLINT DEFAULT 0,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # 2. Documents et Chunks d'Architecture Azure LLMOps
        docs_data = [
            {
                "name": "Azure-Cloud-Architecture-LLMOps.md",
                "file_type": "markdown",
                "file_size": 42560,
                "chunks": [
                    "L'architecture RAG sur Microsoft Azure repose sur Azure Container Apps (serverless FastAPI), Azure Database for PostgreSQL Flexible Server avec l'extension pgvector pour la recherche sémantique hybride, et Azure OpenAI pour l'inférence GPT-5-mini.",
                    "L'isolation réseau et la gouvernance sont assurées par des VNet Azure, du chiffrement TLS 1.3 de bout en bout et un masquage PII automatique en amont des requêtes LLM.",
                    "La recherche hybride combine la similarité cosinus dense calculée par pgvector et la recherche textuelle BM25 (Full Text Search PostgreSQL) via l'algorithme Reciprocal Rank Fusion (RRF).",
                    "Le cache sémantique permet de réduire la latence p95 à moins de 35ms sur les requêtes fréquentes et d'économiser plus de 45% sur les coûts d'inférence Azure OpenAI."
                ]
            },
            {
                "name": "Guide-Gouvernance-Observabilite-2026.pdf",
                "file_type": "pdf",
                "file_size": 128450,
                "chunks": [
                    "L'observabilité de production trace chaque inférence avec Langfuse et Azure Application Insights : latence de récupération (retrieval), nombre de tokens d'entrée/sortie, coût calculé au micro-centime et score d'évaluation automatique.",
                    "Le Quality Gate CI/CD vérifie les scores de fidélité (faithfulness), de pertinence contextuelle et la résistance aux injections de prompts avant chaque déploiement en production.",
                    "L'évaluation LLM-as-a-judge s'exécute sur le Golden Dataset de référence pour détecter tout risque de régression de performance avant la mise en ligne."
                ]
            }
        ]

        import numpy as np

        def generate_embedding(seed_str: str):
            import hashlib
            seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
            np.random.seed(seed)
            v = np.random.randn(settings.VECTOR_DIMENSION).astype(float)
            norm = np.linalg.norm(v)
            return (v / norm).tolist()

        for doc in docs_data:
            doc_id = str(uuid.uuid4())
            conn.execute(text("""
                INSERT INTO indexed_documents (id, name, file_type, chunks_count, file_size_bytes, status)
                VALUES (:id, :name, :ftype, :chunks, :size, 'indexed')
                ON CONFLICT (name) DO UPDATE SET 
                    chunks_count = EXCLUDED.chunks_count,
                    file_size_bytes = EXCLUDED.file_size_bytes;
            """), {
                "id": doc_id,
                "name": doc["name"],
                "ftype": doc["file_type"],
                "chunks": len(doc["chunks"]),
                "size": doc["file_size"]
            })

            for idx, chunk_text in enumerate(doc["chunks"]):
                chunk_id = f"chunk-{doc['name'][:10]}-{idx}"
                embedding = generate_embedding(chunk_text)
                metadata = {
                    "source": doc["name"],
                    "chunk_index": idx,
                    "total_chunks": len(doc["chunks"]),
                    "char_length": len(chunk_text)
                }
                conn.execute(text(f"""
                    INSERT INTO document_chunks (id, content, metadata, embedding)
                    VALUES (:id, :content, :metadata, :embedding)
                    ON CONFLICT (id) DO UPDATE SET
                        content = EXCLUDED.content,
                        metadata = EXCLUDED.metadata;
                """), {
                    "id": chunk_id,
                    "content": chunk_text,
                    "metadata": json.dumps(metadata),
                    "embedding": str(embedding)
                })

        # 3. Conversations et Métriques Réelles de Télémétrie
        telemetry_samples = [
            {
                "query": "Comment l'extension pgvector optimise-t-elle la recherche sémantique ?",
                "answer": "pgvector permet d'indexer les embeddings vectoriels (1536 dimensions) avec des index HNSW et IVFFlat dans PostgreSQL Flexible Server, assurant des recherches par similarité cosinus avec des latences inférieures à 20ms.",
                "latency_ms": 285,
                "retrieval_ms": 18,
                "cost_usd": 0.00038,
                "cache_hit": False,
                "feedback": 1
            },
            {
                "query": "Quel est le rôle du cache sémantique dans l'architecture Azure ?",
                "answer": "Le cache sémantique intercepte les requêtes utilisateur présentant une forte similarité cosinus (>0.92) avec une requête précédente. Cela permet de répondre instantanément en moins de 30ms sans appel payant à Azure OpenAI.",
                "latency_ms": 24,
                "retrieval_ms": 0,
                "cost_usd": 0.0,
                "cache_hit": True,
                "feedback": 1
            },
            {
                "query": "Quels sont les composants clés déployés par Terraform sur Azure ?",
                "answer": "Terraform provisionne le Resource Group, le VNet avec sous-réseaux, Azure Database for PostgreSQL Flexible avec pgvector, le compte Azure OpenAI (avec gpt-chat et text-embedding-3-small), Azure Container Apps, Azure Blob Storage, Log Analytics, Application Insights et Azure Static Web Apps.",
                "latency_ms": 342,
                "retrieval_ms": 22,
                "cost_usd": 0.00046,
                "cache_hit": False,
                "feedback": 1
            },
            {
                "query": "Comment le Quality Gate garantit-il la non-régression du pipeline ?",
                "answer": "Le Quality Gate CI/CD évalue le Golden Dataset avec un modèle juge, exigeant des scores minimaux : fidélité >= 0.85, pertinence >= 0.80 et latence p95 < 800ms. Si un critère échoue, le déploiement est automatiquement bloqué.",
                "latency_ms": 310,
                "retrieval_ms": 19,
                "cost_usd": 0.00041,
                "cache_hit": False,
                "feedback": 1
            },
            {
                "query": "Quels mécanismes de sécurité protègent contre les injections de prompt ?",
                "answer": "Le service de Guardrails analyse chaque invite en amont : détection des tentatives de jailbreak ou de détournement système, masquage des informations personnelles (PII) et blocage immédiat avec trace d'audit si une règle est violée.",
                "latency_ms": 268,
                "retrieval_ms": 15,
                "cost_usd": 0.00036,
                "cache_hit": False,
                "feedback": 1
            },
            {
                "query": "Quelle est la différence entre Azure Container Apps et App Runner ?",
                "answer": "Azure Container Apps repose sur Kubernetes managé (KEDA + Envoy) sous le capot, permettant un scaling automatique à zéro, la prise en charge native des microservices, et une intégration étroite avec Azure Virtual Networks et Log Analytics.",
                "latency_ms": 325,
                "retrieval_ms": 21,
                "cost_usd": 0.00044,
                "cache_hit": False,
                "feedback": 1
            }
        ]

        conv_id = f"conv-demo-{str(uuid.uuid4())[:8]}"
        conn.execute(text("""
            INSERT INTO chat_conversations (id, title, user_id)
            VALUES (:id, :title, 'admin_user')
            ON CONFLICT (id) DO NOTHING;
        """), {"id": conv_id, "title": "Session d'Architecture Cloud Azure & LLMOps"})

        now = datetime.datetime.now(datetime.timezone.utc)
        for i, sample in enumerate(telemetry_samples):
            q_id = f"msg-user-{i}-{str(uuid.uuid4())[:6]}"
            a_id = f"msg-asst-{i}-{str(uuid.uuid4())[:6]}"
            trace_id = f"trace-az-{i}-{str(uuid.uuid4())[:8]}"
            ts_str = (now - datetime.timedelta(minutes=(len(telemetry_samples) - i) * 5)).isoformat()

            # Message utilisateur
            conn.execute(text("""
                INSERT INTO chat_messages (id, conversation_id, role, content, timestamp_str, trace_id)
                VALUES (:id, :cid, 'user', :content, :ts, :trace_id)
                ON CONFLICT (id) DO NOTHING;
            """), {
                "id": q_id,
                "cid": conv_id,
                "content": sample["query"],
                "ts": ts_str,
                "trace_id": trace_id
            })

            # Métriques associées à la réponse
            metrics = {
                "total_latency_ms": sample["latency_ms"],
                "retrieval_latency_ms": sample["retrieval_ms"],
                "cost_usd": sample["cost_usd"],
                "input_tokens": 140 if not sample["cache_hit"] else 0,
                "output_tokens": 65 if not sample["cache_hit"] else 0,
                "cache_hit": sample["cache_hit"],
                "model_id": settings.AZURE_OPENAI_CHAT_DEPLOYMENT if not sample["cache_hit"] else "semantic-cache",
                "prompt_version": PROMPT_VERSION
            }

            conn.execute(text("""
                INSERT INTO chat_messages (
                    id, conversation_id, role, content, timestamp_str, trace_id, 
                    sources, metrics, feedback_given
                )
                VALUES (
                    :id, :cid, 'assistant', :content, :ts, :trace_id, 
                    :sources, :metrics, :feedback
                )
                ON CONFLICT (id) DO NOTHING;
            """), {
                "id": a_id,
                "cid": conv_id,
                "content": sample["answer"],
                "ts": ts_str,
                "trace_id": trace_id,
                "sources": json.dumps([{"source": "Azure-Cloud-Architecture-LLMOps.md", "similarity": 0.89}]),
                "metrics": json.dumps(metrics),
                "feedback": sample["feedback"]
            })

    logger.info("Données initiales Azure et télémétrie injectées avec succès dans PostgreSQL !")

if __name__ == "__main__":
    seed_database()
