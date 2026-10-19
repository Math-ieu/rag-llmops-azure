output "resource_group_name" {
  description = "Nom du Resource Group"
  value       = module.resource_group.name
}

output "postgres_fqdn" {
  description = "FQDN de la base de données PostgreSQL Flexible"
  value       = module.postgres_pgvector.server_fqdn
}

output "azure_openai_endpoint" {
  description = "Endpoint Azure OpenAI"
  value       = module.azure_openai.endpoint
}

output "storage_account_name" {
  description = "Nom du compte Azure Blob Storage"
  value       = module.storage_blob.storage_account_name
}

output "backend_api_url" {
  description = "URL publique de l'API FastAPI sur Azure Container Apps"
  value       = module.container_app.backend_url
}

output "frontend_url" {
  description = "URL publique de l'application Web React sur Azure Static Web Apps"
  value       = module.static_web_app.default_host_name
}

output "application_insights_connection_string" {
  description = "Connection string pour Application Insights"
  value       = module.monitoring.application_insights_connection_string
  sensitive   = true
}
