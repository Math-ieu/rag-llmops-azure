from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "RAG-LLMOps-Azure"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"

    # Cloud Provider Selection
    CLOUD_PROVIDER: str = "azure"  # "azure" ou "aws"

    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_CHAT_DEPLOYMENT: str = "gpt-4o-mini"
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = "text-embedding-3-small"
    AZURE_OPENAI_API_VERSION: str = "2024-06-01"

    # Azure Storage Blob Configuration
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    AZURE_STORAGE_CONTAINER_DOCUMENTS: str = "documents"

    # AWS & Bedrock Fallback (pour compatibilité multi-cloud)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_SESSION_TOKEN: str = ""
    BEDROCK_LLM_MODEL_ID: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    BEDROCK_EMBEDDING_MODEL_ID: str = "amazon.titan-embed-text-v2:0"
    DOCUMENTS_S3_BUCKET: str = ""

    # Mode Simulation / Mock pour tests sans frais Cloud
    MOCK_LLM: bool = Field(
        default=False,
        description="Si activé, simule les réponses LLM/Embeddings sans appel payant (utile pour tests unitaires/CI)"
    )
    MOCK_BEDROCK: bool = Field(
        default=False,
        description="Alias pour compatibilité MOCK_LLM"
    )

    # Database & Vector Store
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/rag_llmops"
    VECTOR_DIMENSION: int = 1536  # Dimension native OpenAI text-embedding-3-small
    SIMILARITY_THRESHOLD: float = 0.55
    TOP_K_CHUNKS: int = 4

    # Langfuse Observability
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    LANGFUSE_ENABLED: bool = True

    # Azure Application Insights & CloudWatch
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = ""
    ENABLE_CLOUDWATCH_METRICS: bool = False
    CLOUDWATCH_NAMESPACE: str = "LLMOps/RAGPlatform"

    # Semantic Cache & Governance
    SEMANTIC_CACHE_ENABLED: bool = True
    SEMANTIC_CACHE_THRESHOLD: float = 0.92  # Cosine similarity threshold for cache hit
    ENABLE_GUARDRAILS: bool = True
    MASK_PII: bool = True
    BEDROCK_GUARDRAIL_ID: str = ""
    BEDROCK_GUARDRAIL_VERSION: str = "DRAFT"


settings = Settings()
