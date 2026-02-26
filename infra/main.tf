# ---------------------------------------------------------------------------
# Data sources – reference existing resources
# ---------------------------------------------------------------------------

data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

# NOTE: The existing 'frankvaneykelen' App Service Plan is Windows.
# Python on Azure App Service requires a Linux plan.
# Either create a new Linux plan below, or reference an existing one.
#
# Option A – create a new Linux plan (uncomment):
# resource "azurerm_service_plan" "linux" {
#   name                = var.app_service_plan_name
#   resource_group_name = data.azurerm_resource_group.main.name
#   location            = data.azurerm_resource_group.main.location
#   os_type             = "Linux"
#   sku_name            = "B1"
# }
#
# Option B – reference an existing Linux plan (default):
data "azurerm_service_plan" "main" {
  name                = var.app_service_plan_name
  resource_group_name = data.azurerm_resource_group.main.name
}

# ---------------------------------------------------------------------------
# Linux Web App (Python 3.12)
# ---------------------------------------------------------------------------

resource "azurerm_linux_web_app" "hellenvanmeene_django" {
  name                = var.app_name
  resource_group_name = data.azurerm_resource_group.main.name
  location            = data.azurerm_resource_group.main.location
  service_plan_id     = data.azurerm_service_plan.main.id

  https_only = true

  identity {
    type = "SystemAssigned"
  }

  site_config {
    always_on       = false
    http2_enabled   = true
    ftps_state      = "Disabled"
    minimum_tls_version = "1.2"

    application_stack {
      python_version = "3.12"
    }

    # Gunicorn startup command
    app_command_line = "gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 120"
  }

  app_settings = {
    # Django runtime settings
    DJANGO_SETTINGS_MODULE = "config.settings.prod"

    # Secrets sourced from Key Vault references (managed identity resolves these)
    SECRET_KEY       = "@Microsoft.KeyVault(VaultName=${var.key_vault_name};SecretName=DjangoSecretKey)"
    DB_PASSWORD      = "@Microsoft.KeyVault(VaultName=${var.key_vault_name};SecretName=DbPassword)"
    SENDGRID_API_KEY = "@Microsoft.KeyVault(VaultName=${var.key_vault_name};SecretName=SendGridApiKey)"
    AZURE_ACCOUNT_KEY = "@Microsoft.KeyVault(VaultName=${var.key_vault_name};SecretName=AzureAccountKey)"

    # Non-sensitive DB config
    DB_HOST = var.db_host
    DB_NAME = var.db_name
    DB_USER = var.db_user
    DB_PORT = "1433"

    # Storage
    AZURE_ACCOUNT_NAME = var.azure_account_name
    AZURE_CONTAINER    = var.azure_container

    # Disable Django static file collection to stdout during startup
    DISABLE_COLLECTSTATIC = "0"

    # SCM build
    SCM_DO_BUILD_DURING_DEPLOYMENT = "true"
  }

  tags = {
    environment = "production"
    project     = "hellenvanmeene"
    runtime     = "python"
  }
}

# ---------------------------------------------------------------------------
# Custom hostname bindings
# ---------------------------------------------------------------------------

resource "azurerm_app_service_custom_hostname_binding" "custom_domains" {
  for_each = toset(var.custom_hostnames)

  hostname            = each.value
  app_service_name    = azurerm_linux_web_app.hellenvanmeene_django.name
  resource_group_name = data.azurerm_resource_group.main.name
}
