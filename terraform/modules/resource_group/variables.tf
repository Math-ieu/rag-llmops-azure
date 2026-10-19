variable "resource_group_name" {
  description = "Nom du Resource Group Azure"
  type        = string
}

variable "location" {
  description = "Région Azure de déploiement (ex: eastus, francecentral)"
  type        = string
  default     = "eastus"
}

variable "tags" {
  description = "Tags appliqués aux ressources"
  type        = map(string)
  default     = {}
}
