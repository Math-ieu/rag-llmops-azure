variable "resource_group_name" {
  description = "Nom du Resource Group"
  type        = string
}

variable "location" {
  description = "Région Azure pour Static Web App (ex: westeurope, eastus2)"
  type        = string
  default     = "westeurope"
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

variable "tags" {
  description = "Tags"
  type        = map(string)
  default     = {}
}
