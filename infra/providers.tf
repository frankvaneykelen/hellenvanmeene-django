terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  # Store state remotely – uncomment and fill in after creating the storage account
  # backend "azurerm" {
  #   resource_group_name  = "frankvaneykelen-blog"
  #   storage_account_name = "<tf-state-storage-account>"
  #   container_name       = "tfstate"
  #   key                  = "hellenvanmeene-django.tfstate"
  # }
}

provider "azurerm" {
  subscription_id = var.subscription_id
  features {}
}
