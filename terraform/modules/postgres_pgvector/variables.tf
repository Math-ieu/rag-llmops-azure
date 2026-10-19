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
  description = "Environnement (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "server_name_suffix" {
  description = "Suffixe unique aléatoire pour le nom du serveur"
  type        = string
  default     = ""
}

variable "db_username" {
  description = "Nom d'utilisateur administrateur"
  type        = string
  default     = "ragadmin"
}

variable "db_password" {
  description = "Mot de passe administrateur"
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "Nom de la base de données"
  type        = string
  default     = "rag_llmops"
}

variable "sku_name" {
  description = "SKU du serveur flexible PostgreSQL (Burstable pour coûts réduits)"
  type        = string
  default     = "B_Standard_B1ms"
}

variable "storage_mb" {
  description = "Taille de stockage en Mo"
  type        = number
  default     = 32768
}

variable "tags" {
  description = "Tags"
  type        = map(string)
  default     = {}
}
