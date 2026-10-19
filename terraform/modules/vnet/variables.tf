variable "resource_group_name" {
  description = "Nom du Resource Group"
  type        = string
}

variable "location" {
  description = "Région Azure"
  type        = string
}

variable "vnet_name" {
  description = "Nom du Virtual Network"
  type        = string
}

variable "address_space" {
  description = "Plage CIDR du VNet"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "tags" {
  description = "Tags"
  type        = map(string)
  default     = {}
}
