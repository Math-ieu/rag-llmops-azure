locals {
  clean_project = lower(replace(var.project_name, "_", "-"))
}

resource "azurerm_container_app_environment" "env" {
  name                       = "cae-${local.clean_project}-${var.environment}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  log_analytics_workspace_id = var.log_analytics_workspace_id

  tags = var.tags
}

resource "azurerm_container_app" "backend" {
  name                         = "ca-${local.clean_project}-backend-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = var.resource_group_name
  revision_mode                = "Single"

  template {
    min_replicas = 0
    max_replicas = 2

    container {
      name   = "rag-backend"
      image  = var.container_image
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "APP_ENV"
        value = var.environment
      }
      env {
        name  = "DATABASE_URL"
        value = var.database_url
      }
      env {
        name  = "AZURE_OPENAI_ENDPOINT"
        value = var.azure_openai_endpoint
      }
      env {
        name  = "AZURE_OPENAI_API_KEY"
        value = var.azure_openai_api_key
      }
      env {
        name  = "AZURE_OPENAI_CHAT_DEPLOYMENT"
        value = var.azure_openai_chat_deployment
      }
      env {
        name  = "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
        value = var.azure_openai_embedding_deployment
      }
      env {
        name  = "AZURE_STORAGE_CONNECTION_STRING"
        value = var.blob_storage_connection_string
      }
      env {
        name  = "AZURE_STORAGE_CONTAINER_DOCUMENTS"
        value = var.blob_container_name
      }
      env {
        name  = "LANGFUSE_PUBLIC_KEY"
        value = var.langfuse_public_key
      }
      env {
        name  = "LANGFUSE_SECRET_KEY"
        value = var.langfuse_secret_key
      }
      env {
        name  = "LANGFUSE_HOST"
        value = var.langfuse_host
      }
      env {
        name  = "VECTOR_DIMENSION"
        value = "1536" # Dimension native standard text-embedding-3-small
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    transport        = "auto"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  tags = var.tags
}
