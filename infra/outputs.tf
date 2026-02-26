output "web_app_id" {
  description = "Resource ID of the web app"
  value       = azurerm_linux_web_app.hellenvanmeene_django.id
}

output "default_hostname" {
  description = "Default azurewebsites.net hostname"
  value       = azurerm_linux_web_app.hellenvanmeene_django.default_hostname
}

output "custom_domain_verification_id" {
  description = "Add as TXT record (asuid.<hostname>) to verify domain ownership"
  value       = azurerm_linux_web_app.hellenvanmeene_django.custom_domain_verification_id
  sensitive   = true
}

output "outbound_ip_addresses" {
  description = "Outbound IPs – use the first for A record DNS"
  value       = azurerm_linux_web_app.hellenvanmeene_django.outbound_ip_addresses
}

output "portal_url" {
  description = "Direct link to the resource in Azure Portal"
  value       = "https://portal.azure.com/#resource${azurerm_linux_web_app.hellenvanmeene_django.id}"
}

output "key_vault_uri" {
  description = "URI of the Key Vault"
  value       = data.azurerm_key_vault.main.vault_uri
}

output "web_app_principal_id" {
  description = "Object ID of the web app's system-assigned managed identity"
  value       = azurerm_linux_web_app.hellenvanmeene_django.identity[0].principal_id
}
