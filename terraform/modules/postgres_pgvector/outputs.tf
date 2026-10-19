output "server_id" {
  description = "ID du serveur PostgreSQL Flexible"
  value       = azurerm_postgresql_flexible_server.postgres.id
}

output "server_fqdn" {
  description = "FQDN d'accès au serveur PostgreSQL"
  value       = azurerm_postgresql_flexible_server.postgres.fqdn
}

output "database_name" {
  description = "Nom de la base de données RAG"
  value       = azurerm_postgresql_flexible_server_database.rag_db.name
}

output "connection_string" {
  description = "Chaîne de connexion SQLAlchemy / asyncpg"
  value       = "postgresql://${var.db_username}:${var.db_password}@${azurerm_postgresql_flexible_server.postgres.fqdn}:5432/${var.db_name}?sslmode=require"
  sensitive   = true
}
