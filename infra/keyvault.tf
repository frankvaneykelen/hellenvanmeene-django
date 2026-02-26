# ---------------------------------------------------------------------------
# Key Vault – reference existing vault and store Django secrets
# ---------------------------------------------------------------------------

data "azurerm_key_vault" "main" {
  name                = var.key_vault_name
  resource_group_name = data.azurerm_resource_group.main.name
}

# Grant the web app's managed identity read access to secrets
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault_access_policy" "web_app" {
  key_vault_id = data.azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_linux_web_app.hellenvanmeene_django.identity[0].principal_id

  secret_permissions = ["Get", "List"]
}

# ---------------------------------------------------------------------------
# Secrets (values read from secrets.tfvars, never committed)
# ---------------------------------------------------------------------------

resource "azurerm_key_vault_secret" "django_secret_key" {
  name         = "DjangoSecretKey"
  value        = var.secret_key
  key_vault_id = data.azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "db_password" {
  name         = "DbPassword"
  value        = var.db_password
  key_vault_id = data.azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "sendgrid_api_key" {
  name         = "SendGridApiKey"
  value        = var.sendgrid_api_key
  key_vault_id = data.azurerm_key_vault.main.id
}

resource "azurerm_key_vault_secret" "azure_account_key" {
  name         = "AzureAccountKey"
  value        = var.azure_account_key
  key_vault_id = data.azurerm_key_vault.main.id
}
