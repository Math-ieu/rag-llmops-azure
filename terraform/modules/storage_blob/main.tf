locals {
  # Nom du compte de stockage Azure : max 24 caractères, minuscules alphanumériques uniquement
  clean_name = substr(lower(replace("${var.project_name}${var.environment}${var.storage_account_suffix}", "/[^a-z0-9]/", "")), 0, 24)
}

resource "azurerm_storage_account" "storage" {
  name                     = local.clean_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"

  blob_properties {
    versioning_enabled = true
    delete_retention_policy {
      days = 14
    }
  }

  tags = var.tags
}

resource "azurerm_storage_container" "documents" {
  name                  = "documents"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "datasets" {
  name                  = "datasets"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}
