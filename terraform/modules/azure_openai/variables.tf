variable "resource_group_name" {
  description = "Nom du Resource Group"
  type        = string
}

variable "location" {
  description = "Région Azure (recommandé: eastus ou swedencentral pour OpenAI)"
  type        = string
  default     = "eastus"
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

variable "openai_account_suffix" {
  description = "Suffixe unique aléatoire pour le compte Cognitive Service"
  type        = string
  default     = ""
}

variable "chat_deployment_name" {
  description = "Nom du déploiement pour le modèle de discussion"
  type        = string
  default     = "gpt-4o-mini"
}

variable "chat_model_name" {
  description = "Modèle OpenAI de chat"
  type        = string
  default     = "gpt-4o-mini"
}

variable "chat_model_version" {
  description = "Version du modèle de chat"
  type        = string
  default     = "2024-07-18"
}

variable "chat_capacity" {
  description = "Capacité TPM (en milliers de tokens par minute, ex: 10 = 10k TPM)"
  type        = number
  default     = 10
}

variable "embedding_deployment_name" {
  description = "Nom du déploiement pour les embeddings"
  type        = string
  default     = "text-embedding-3-small"
}

variable "embedding_model_name" {
  description = "Modèle OpenAI d'embeddings"
  type        = string
  default     = "text-embedding-3-small"
}

variable "embedding_model_version" {
  description = "Version du modèle d'embeddings"
  type        = string
  default     = "1"
}

variable "embedding_capacity" {
  description = "Capacité TPM d'embeddings"
  type        = number
  default     = 10
}

variable "tags" {
  description = "Tags"
  type        = map(string)
  default     = {}
}
