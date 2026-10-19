output "backend_url" {
  description = "URL publique HTTPS du backend FastAPI sur Azure Container Apps"
  value       = "https://${azurerm_container_app.backend.ingress[0].fqdn}"
}

output "container_app_id" {
  value = azurerm_container_app.backend.id
}

output "environment_id" {
  value = azurerm_container_app_environment.env.id
}
