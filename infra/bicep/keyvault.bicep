// Deployed as a module scoped to the Key Vault's resource group
// (subscription 3c0a1e74 / hellenvanmeene).
// Called from main.bicep with an explicit cross-subscription scope.

@description('Name of the existing Key Vault.')
param keyVaultName string

@description('Principal ID of the web app managed identity that needs KV access.')
param webAppPrincipalId string

@description('Tenant ID (same for both subscriptions).')
param tenantId string = tenant().tenantId

@description('Django SECRET_KEY.')
@secure()
param secretKey string

@description('Azure SQL password.')
@secure()
param dbPassword string

@description('SendGrid API key.')
@secure()
param sendgridApiKey string

@description('Azure Blob Storage account key.')
@secure()
param azureAccountKey string

// -------------------------------------------------------------------------
// Existing Key Vault (in scope — no cross-subscription reference needed here)
// -------------------------------------------------------------------------

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

// -------------------------------------------------------------------------
// Grant managed identity read access to secrets
// -------------------------------------------------------------------------

resource kvAccessPolicy 'Microsoft.KeyVault/vaults/accessPolicies@2023-07-01' = {
  parent: keyVault
  name: 'add'
  properties: {
    accessPolicies: [
      {
        tenantId: tenantId
        objectId: webAppPrincipalId
        permissions: {
          secrets: [
            'get'
            'list'
          ]
        }
      }
    ]
  }
}

// -------------------------------------------------------------------------
// Secrets
// -------------------------------------------------------------------------

resource secretDjangoKey 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'DjangoSecretKey'
  properties: {
    value: secretKey
  }
}

resource secretDbPassword 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'DbPassword'
  properties: {
    value: dbPassword
  }
}

resource secretSendgrid 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'SendGridApiKey'
  properties: {
    value: sendgridApiKey
  }
}

resource secretStorageKey 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'AzureAccountKey'
  properties: {
    value: azureAccountKey
  }
}

// -------------------------------------------------------------------------
// Outputs
// -------------------------------------------------------------------------

output keyVaultUri string = keyVault.properties.vaultUri
