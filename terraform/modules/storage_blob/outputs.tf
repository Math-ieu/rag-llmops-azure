output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}

output "storage_account_id" {
  value = azurerm_storage_account.storage.id
}

output "primary_access_key" {
  value     = azurerm_storage_account.storage.primary_access_key
  sensitive = true
}

output "primary_connection_string" {
  value     = azurerm_storage_account.storage.primary_connection_string
  sensitive = true
}

output "primary_blob_endpoint" {
  value = azurerm_storage_account.storage.primary_blob_endpoint
}

output "documents_container_name" {
  value = azurerm_storage_container.documents.name
}

output "datasets_container_name" {
  value = azurerm_storage_container.datasets.name
}
