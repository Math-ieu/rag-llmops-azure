variable "resource_group_name" {
  description = "Nom du Resource Group"
  type        = string
}

variable "location" {
  description = "Région Azure"
  type        = string
}

variable "project_name" {
  description = "Nom du projet"
  type        = string
}

variable "environment" {
  description = "Environnement"
  type        = string
  default     = "dev"
}

variable "log_analytics_workspace_id" {
  description = "ID du Log Analytics Workspace pour le monitoring"
  type        = string
}

variable "container_image" {
  description = "Image Docker pour le backend FastAPI"
  type        = string
  default     = "mcr.microsoft.com/azuredocs/aci-helloworld:latest"
}

variable "database_url" {
  description = "Chaîne de connexion SQLAlchemy PostgreSQL"
  type        = string
  sensitive   = true
}

variable "azure_openai_endpoint" {
  description = "Endpoint du service Azure OpenAI"
  type        = string
  default     = ""
}

variable "azure_openai_api_key" {
  description = "Clé API Azure OpenAI"
  type        = string
  default     = ""
  sensitive   = true
}

variable "azure_openai_chat_deployment" {
  description = "Nom du déploiement de chat (ex: gpt-4o-mini)"
  type        = string
  default     = "gpt-4o-mini"
}

variable "azure_openai_embedding_deployment" {
  description = "Nom du déploiement d'embedding (ex: text-embedding-3-small)"
  type        = string
  default     = "text-embedding-3-small"
}

variable "blob_storage_connection_string" {
  description = "Chaîne de connexion au compte de stockage Azure Blob"
  type        = string
  default     = ""
  sensitive   = true
}

variable "blob_container_name" {
  description = "Nom du container Blob pour les documents"
  type        = string
  default     = "documents"
}

variable "langfuse_public_key" {
  description = "Clé publique Langfuse"
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
  description = "Hôte Langfuse"
  type        = string
  default     = "https://cloud.langfuse.com"
}

variable "tags" {
  description = "Tags"
  type        = map(string)
  default     = {}
}
