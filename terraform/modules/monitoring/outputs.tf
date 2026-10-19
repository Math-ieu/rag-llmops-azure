output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.log_analytics.id
}

output "application_insights_id" {
  value = azurerm_application_insights.app_insights.id
}

output "application_insights_connection_string" {
  value     = azurerm_application_insights.app_insights.connection_string
  sensitive = true
}

output "application_insights_instrumentation_key" {
  value     = azurerm_application_insights.app_insights.instrumentation_key
  sensitive = true
}
