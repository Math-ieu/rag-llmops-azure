locals {
  clean_project = lower(replace(var.project_name, "_", "-"))
  server_name   = var.server_name_suffix != "" ? "psql-${local.clean_project}-${var.environment}-${var.server_name_suffix}" : "psql-${local.clean_project}-${var.environment}"
}

resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = local.server_name
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "16"
  administrator_login    = var.db_username
  administrator_password = var.db_password
  sku_name               = var.sku_name
  storage_mb             = var.storage_mb
  backup_retention_days  = 7
  geo_redundant_backup_enabled = false

  tags = var.tags

  lifecycle {
    ignore_changes = [
      zone
    ]
  }
}

# Activation de l'extension pgvector pour la recherche sémantique & HNSW
resource "azurerm_postgresql_flexible_server_configuration" "pgvector" {
  name      = "azure.extensions"
  server_id = azurerm_postgresql_flexible_server.postgres.id
  value     = "vector"
}

# Base de données applicative
resource "azurerm_postgresql_flexible_server_database" "rag_db" {
  name      = var.db_name
  server_id = azurerm_postgresql_flexible_server.postgres.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# Règle de pare-feu : autoriser les services internes Azure (Container Apps, etc.)
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.postgres.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
