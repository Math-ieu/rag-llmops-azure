locals {
  clean_project = lower(replace(var.project_name, "_", "-"))
}

resource "azurerm_static_web_app" "frontend" {
  name                = "swa-${local.clean_project}-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku_tier            = "Free"
  sku_size            = "Free"

  tags = var.tags
}
