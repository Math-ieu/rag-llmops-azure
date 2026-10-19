output "default_host_name" {
  description = "URL par défaut de la Static Web App"
  value       = "https://${azurerm_static_web_app.frontend.default_host_name}"
}

output "api_key" {
  description = "Clé de déploiement (Deployment Token) pour GitHub Actions"
  value       = azurerm_static_web_app.frontend.api_key
  sensitive   = true
}
