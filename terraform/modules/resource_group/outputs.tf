output "name" {
  description = "Nom du Resource Group créé"
  value       = azurerm_resource_group.rg.name
}

output "location" {
  description = "Localisation du Resource Group"
  value       = azurerm_resource_group.rg.location
}

output "id" {
  description = "ID du Resource Group"
  value       = azurerm_resource_group.rg.id
}
