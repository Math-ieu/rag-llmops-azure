terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.110"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
    cognitive_account {
      purge_soft_delete_on_destroy = true
    }
  }
}

resource "random_string" "suffix" {
  length  = 5
  special = false
  upper   = false
}

locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    Cloud       = "Azure"
  }
  rg_name = "rg-${var.project_name}-${var.environment}"
}

# 1. Groupe de ressources Azure
module "resource_group" {
  source              = "./modules/resource_group"
  resource_group_name = local.rg_name
  location            = var.azure_location
  tags                = local.common_tags
}

# 2. Réseau virtuel Azure (VNet & Subnets)
module "vnet" {
  source              = "./modules/vnet"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  vnet_name           = "vnet-${var.project_name}-${var.environment}"
  address_space       = ["10.0.0.0/16"]
  tags                = local.common_tags
}

# 3. Base de données PostgreSQL Flexible Server avec extension pgvector
module "postgres_pgvector" {
  source             = "./modules/postgres_pgvector"
  resource_group_name = module.resource_group.name
  location           = module.resource_group.location
  project_name       = var.project_name
  environment        = var.environment
  server_name_suffix = random_string.suffix.result
  db_username        = var.db_username
  db_password        = var.db_password
  sku_name           = var.db_sku_name
  tags               = local.common_tags
}

# 4. Compte de stockage Azure Blob (Documents PDF & Golden Datasets)
module "storage_blob" {
  source                 = "./modules/storage_blob"
  resource_group_name    = module.resource_group.name
  location               = module.resource_group.location
  project_name           = var.project_name
  environment            = var.environment
  storage_account_suffix = random_string.suffix.result
  tags                   = local.common_tags
}

# 5. Service Azure OpenAI (GPT-4o & text-embedding-3)
module "azure_openai" {
  source                    = "./modules/azure_openai"
  resource_group_name       = module.resource_group.name
  location                  = var.azure_location
  project_name              = var.project_name
  environment               = var.environment
  openai_account_suffix     = random_string.suffix.result
  chat_deployment_name      = var.chat_deployment_name
  embedding_deployment_name = var.embedding_deployment_name
  tags                      = local.common_tags
}

# 6. Observabilité & Monitoring (Log Analytics + Application Insights)
module "monitoring" {
  source              = "./modules/monitoring"
  resource_group_name = module.resource_group.name
  location            = module.resource_group.location
  project_name        = var.project_name
  environment         = var.environment
  tags                = local.common_tags
}

# 7. Backend FastAPI sur Azure Container Apps (ACA Serverless)
module "container_app" {
  source                            = "./modules/container_app"
  resource_group_name               = module.resource_group.name
  location                          = module.resource_group.location
  project_name                      = var.project_name
  environment                       = var.environment
  log_analytics_workspace_id        = module.monitoring.log_analytics_workspace_id
  container_image                   = var.container_image
  database_url                      = module.postgres_pgvector.connection_string
  azure_openai_endpoint             = module.azure_openai.endpoint
  azure_openai_api_key              = module.azure_openai.primary_key
  azure_openai_chat_deployment      = module.azure_openai.chat_deployment_name
  azure_openai_embedding_deployment = module.azure_openai.embedding_deployment_name
  blob_storage_connection_string    = module.storage_blob.primary_connection_string
  blob_container_name               = module.storage_blob.documents_container_name
  langfuse_public_key               = var.langfuse_public_key
  langfuse_secret_key               = var.langfuse_secret_key
  langfuse_host                     = var.langfuse_host
  tags                              = local.common_tags
}

# 8. Frontend React sur Azure Static Web Apps
module "static_web_app" {
  source              = "./modules/static_web_app"
  resource_group_name = module.resource_group.name
  location            = "westeurope" # Région supportée pour Static Web Apps
  project_name        = var.project_name
  environment         = var.environment
  tags                = local.common_tags
}
