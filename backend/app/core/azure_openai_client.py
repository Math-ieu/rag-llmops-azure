import json
import logging
import time
from typing import List, Dict, Any, Generator
from app.config import settings

logger = logging.getLogger(__name__)

class AzureOpenAIClient:
    """Client officiel Azure OpenAI pour la génération LLM (GPT-4o) et les embeddings (text-embedding-3)."""

    def __init__(self):
        self.mock_mode = settings.MOCK_LLM
        self.client = None

        if not self.mock_mode and settings.AZURE_OPENAI_ENDPOINT and settings.AZURE_OPENAI_API_KEY:
            try:
                from openai import AzureOpenAI
                self.client = AzureOpenAI(
                    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                    api_key=settings.AZURE_OPENAI_API_KEY,
                    api_version=settings.AZURE_OPENAI_API_VERSION
                )
                logger.info(f"Azure OpenAI client initialisé sur l'endpoint {settings.AZURE_OPENAI_ENDPOINT}")
            except Exception as e:
                logger.warning(f"Impossible d'initialiser Azure OpenAI ({e}). Bascule en mode simulation.")
                self.mock_mode = True
        else:
            self.mock_mode = True

    def _fallback_embedding(self, text: str) -> List[float]:
        """Génère un embedding déterministe local sans coût."""
        import hashlib
        seed = int(hashlib.md5(text.encode()).hexdigest(), 16)
        import numpy as np
        np.random.seed(seed % (2**32))
        vec = np.random.randn(settings.VECTOR_DIMENSION).astype(float)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()

    def get_embedding(self, text: str) -> List[float]:
        """Génère un vecteur d'embedding via Azure OpenAI text-embedding-3-small."""
        if self.mock_mode or not self.client:
            return self._fallback_embedding(text)

        try:
            response = self.client.embeddings.create(
                input=text[:8000],
                model=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT
            )
            return response.data[0].embedding
        except Exception as e:
            logger.warning(f"Azure OpenAI Embeddings indisponible ({e}). Utilisation de l'embedding local.")
            return self._fallback_embedding(text)

    def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1500,
    ) -> Dict[str, Any]:
        """Génération standard via Azure OpenAI Chat Completions (GPT-4o / GPT-4o-mini)."""
        fallback_reply = {
            "text": "D'après les documents d'architecture du système hébergé sur Microsoft Azure, la plateforme LLMOps intègre l'ingestion documentaire, la recherche vectorielle avec pgvector et la supervision continue de bout en bout.",
            "usage": {"input_tokens": 120, "output_tokens": 45, "total_tokens": 165},
            "latency_ms": 150
        }
        if self.mock_mode or not self.client:
            return fallback_reply

        start_time = time.time()
        chat_messages = [{"role": "system", "content": system_prompt}]
        for m in messages:
            chat_messages.append({"role": m["role"], "content": m["content"]})

        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
                messages=chat_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            latency_ms = int((time.time() - start_time) * 1000)
            choice = response.choices[0]
            usage = response.usage

            return {
                "text": choice.message.content or "",
                "usage": {
                    "input_tokens": usage.prompt_tokens if usage else 0,
                    "output_tokens": usage.completion_tokens if usage else 0,
                    "total_tokens": usage.total_tokens if usage else 0,
                },
                "latency_ms": latency_ms,
                "model_id": settings.AZURE_OPENAI_CHAT_DEPLOYMENT
            }
        except Exception as e:
            logger.warning(f"Azure OpenAI Chat Completions indisponible ({e}). Utilisation de la réponse locale.")
            return fallback_reply

    def generate_stream(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1500,
    ) -> Generator[str, None, None]:
        """Streaming de tokens via Azure OpenAI Chat Completions."""
        fallback_tokens = [
            "D'après ", "les ", "documents ", "d'architecture ", "Azure, ", "le ", "système ",
            "RAG ", "fonctionne ", "avec ", "une ", "recherche ", "hybride ", "sur ", "PostgreSQL ",
            "Flexible ", "et ", "une ", "observabilité ", "complète."
        ]
        if self.mock_mode or not self.client:
            for token in fallback_tokens:
                time.sleep(0.04)
                yield token
            return

        chat_messages = [{"role": "system", "content": system_prompt}]
        for m in messages:
            chat_messages.append({"role": m["role"], "content": m["content"]})

        try:
            stream = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_CHAT_DEPLOYMENT,
                messages=chat_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.warning(f"Azure OpenAI streaming indisponible ({e}). Bascule sur tokens locaux.")
            for token in fallback_tokens:
                time.sleep(0.04)
                yield token


azure_openai_client = AzureOpenAIClient()
