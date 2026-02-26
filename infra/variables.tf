variable "subscription_id" {
  type        = string
  description = "Target Azure subscription ID"
}

variable "resource_group_name" {
  type        = string
  description = "Name of the resource group in the target subscription"
  default     = "frankvaneykelen-blog"
}

variable "app_service_plan_name" {
  type        = string
  description = "Name of the existing App Service Plan (must be Linux-based)"
  default     = "frankvaneykelen-linux"
}

variable "app_name" {
  type        = string
  description = "Name of the web app (globally unique on azurewebsites.net)"
  default     = "hellenvanmeene-django"
}

variable "location" {
  type        = string
  description = "Azure region – must match the App Service Plan's region"
  default     = "westeurope"
}

variable "key_vault_name" {
  type        = string
  description = "Existing Key Vault name"
  default     = "hellenvanmeene-kv"
}

variable "custom_hostnames" {
  type        = list(string)
  description = "Custom hostnames to bind. DNS must point to the app first."
  default = [
    "hellenvanmeene.com",
    "www.hellenvanmeene.com",
    "hellenvanmeene.net",
    "www.hellenvanmeene.net",
    "hellenvanmeene.nl",
    "www.hellenvanmeene.nl",
  ]
}

# ---------------------------------------------------------------------------
# Secrets – passed via secrets.tfvars (never committed)
# ---------------------------------------------------------------------------

variable "secret_key" {
  type        = string
  description = "Django SECRET_KEY"
  sensitive   = true
}

variable "db_password" {
  type        = string
  description = "Azure SQL password"
  sensitive   = true
}

variable "db_host" {
  type        = string
  description = "Azure SQL server hostname"
}

variable "db_name" {
  type        = string
  description = "Azure SQL database name"
  default     = "HellenvanMeene"
}

variable "db_user" {
  type        = string
  description = "Azure SQL user"
}

variable "azure_account_name" {
  type        = string
  description = "Azure Blob Storage account name"
}

variable "azure_account_key" {
  type        = string
  description = "Azure Blob Storage account key"
  sensitive   = true
}

variable "azure_container" {
  type        = string
  description = "Azure Blob Storage container name"
  default     = "photos"
}

variable "sendgrid_api_key" {
  type        = string
  description = "SendGrid API key"
  sensitive   = true
}
