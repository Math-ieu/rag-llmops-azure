locals {
  clean_project = lower(replace(var.project_name, "_", "-"))
  account_name  = var.openai_account_suffix != "" ? "oai-${local.clean_project}-${var.environment}-${var.openai_account_suffix}" : "oai-${local.clean_project}-${var.environment}"
}

resource "azurerm_cognitive_account" "openai" {
  name                  = local.account_name
  location              = var.location
  resource_group_name   = var.resource_group_name
  kind                  = "OpenAI"
  sku_name              = "S0"
  custom_subdomain_name = local.account_name

  tags = var.tags
}

# Déploiement du modèle LLM de génération (ex: gpt-4o-mini)
resource "azurerm_cognitive_deployment" "chat" {
  name                 = var.chat_deployment_name
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = var.chat_model_name
    version = var.chat_model_version
  }

  scale {
    type     = "Standard"
    capacity = var.chat_capacity
  }
}

# Déploiement du modèle d'embeddings vectoriels (ex: text-embedding-3-small)
resource "azurerm_cognitive_deployment" "embeddings" {
  name                 = var.embedding_deployment_name
  cognitive_account_id = azurerm_cognitive_account.openai.id

  model {
    format  = "OpenAI"
    name    = var.embedding_model_name
    version = var.embedding_model_version
  }

  scale {
    type     = "Standard"
    capacity = var.embedding_capacity
  }
}
