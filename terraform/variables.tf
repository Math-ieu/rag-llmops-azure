variable "azure_location" {
  description = "Région principale de déploiement Azure"
  type        = string
  default     = "eastus"
}

variable "project_name" {
  description = "Nom du projet LLMOps"
  type        = string
  default     = "rag-llmops"
}

variable "environment" {
  description = "Environnement cible (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "db_username" {
  description = "Nom d'utilisateur administrateur PostgreSQL"
  type        = string
  default     = "ragadmin"
}

variable "db_password" {
  description = "Mot de passe administrateur PostgreSQL"
  type        = string
  sensitive   = true
  default     = "P@ssw0rdSecureLLMOps2026!"
}

variable "db_sku_name" {
  description = "SKU pour PostgreSQL Flexible Server"
  type        = string
  default     = "B_Standard_B1ms"
}

variable "chat_deployment_name" {
  description = "Nom du modèle de discussion déployé sur Azure OpenAI"
  type        = string
  default     = "gpt-4o-mini"
}

variable "embedding_deployment_name" {
  description = "Nom du modèle d'embeddings déployé sur Azure OpenAI"
  type        = string
  default     = "text-embedding-3-small"
}

variable "container_image" {
  description = "Image Docker du backend FastAPI"
  type        = string
  default     = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
}

variable "langfuse_public_key" {
  description = "Clé publique Langfuse pour le tracing LLM"
  type        = string
  default     = ""
}

variable "langfuse_secret_key" {
  description = "Clé secrète Langfuse"
  type        = string
  default     = ""
  sensitive   = true
}

variable "langfuse_host" {
  description = "URL de l'instance Langfuse"
  type        = string
  default     = "https://cloud.langfuse.com"
}
