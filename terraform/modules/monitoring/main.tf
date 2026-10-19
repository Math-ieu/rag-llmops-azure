locals {
  clean_project = lower(replace(var.project_name, "_", "-"))
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = "log-${local.clean_project}-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = var.tags
}

resource "azurerm_application_insights" "app_insights" {
  name                = "appi-${local.clean_project}-${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  workspace_id        = azurerm_log_analytics_workspace.log_analytics.id
  application_type    = "web"

  tags = var.tags
}
