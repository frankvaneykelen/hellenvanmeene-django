// hellenvanmeene-django — Azure infrastructure
// Deploys: new Linux B1 App Service Plan, Linux Web App (Python 3.12),
//          Key Vault access policy + secrets, custom hostname bindings.
// The Key Vault itself must already exist (created separately).
//
// Deploy:
//   az deployment group create \
//     --resource-group hellenvanmeene \
//     --parameters main.bicepparam secrets.bicepparam

// -------------------------------------------------------------------------
// Parameters — non-sensitive
// -------------------------------------------------------------------------

@description('Azure region. Must match the Key Vault region.')
param location string = 'westeurope'

@description('Name for the new Linux App Service Plan.')
param appServicePlanName string = 'hellenvanmeene-linux'

@description('Web app name — globally unique on azurewebsites.net.')
param appName string = 'hellenvanmeene-django'

@description('Name of the existing Key Vault.')
param keyVaultName string = 'hellenvanmeene-kv'

@description('Subscription ID that contains the Key Vault (may differ from the deployment subscription).')
param kvSubscriptionId string = '3c0a1e74-fe18-4403-ad5d-e6550f162731'

@description('Resource group that contains the Key Vault.')
param kvResourceGroupName string = 'frankvaneykelen-blog'

@description('Custom hostnames to bind. DNS must be pointed at the app first.')
param customHostnames string[] = [
  'hellenvanmeene.com'
  'www.hellenvanmeene.com'
  'hellenvanmeene.net'
  'www.hellenvanmeene.net'
  'hellenvanmeene.nl'
  'www.hellenvanmeene.nl'
]

@description('Azure SQL server hostname (e.g. server.database.windows.net).')
param dbHost string

@description('Azure SQL database name.')
param dbName string = 'HellenvanMeene'

@description('Azure SQL username.')
param dbUser string

@description('Azure Blob Storage account name.')
param azureAccountName string

@description('Azure Blob Storage container name.')
param azureContainer string = 'photos'

// -------------------------------------------------------------------------
// Parameters — secrets (never committed, supplied via CLI or CI/CD)
// -------------------------------------------------------------------------

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
// Key Vault module — scoped to the KV's subscription + resource group
// BCP165 requires cross-subscription resources to live in a separate module.
// -------------------------------------------------------------------------

module kv './keyvault.bicep' = {
  scope: resourceGroup(kvSubscriptionId, kvResourceGroupName)
  params: {
    keyVaultName: keyVaultName
    webAppPrincipalId: webApp.identity.principalId
    secretKey: secretKey
    dbPassword: dbPassword
    sendgridApiKey: sendgridApiKey
    azureAccountKey: azureAccountKey
  }
}

// -------------------------------------------------------------------------
// App Service Plan — new Linux B1
// -------------------------------------------------------------------------

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  sku: {
    name: 'B1'
    tier: 'Basic'
    size: 'B1'
    family: 'B'
    capacity: 1
  }
  properties: {
    reserved: true // required for Linux
  }
  tags: {
    environment: 'production'
    project: 'hellenvanmeene'
    runtime: 'python'
  }
}

// -------------------------------------------------------------------------
// Web App — Linux, Python 3.12
// -------------------------------------------------------------------------

resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      appCommandLine: 'gunicorn config.wsgi:application --bind 0.0.0.0:8000'
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      appSettings: [
        { name: 'DJANGO_SETTINGS_MODULE', value: 'config.settings.prod' }
        // Secrets resolved at runtime via managed identity → Key Vault
        { name: 'SECRET_KEY', value: '@Microsoft.KeyVault(VaultName=${keyVaultName};SecretName=DjangoSecretKey)' }
        { name: 'DB_PASSWORD', value: '@Microsoft.KeyVault(VaultName=${keyVaultName};SecretName=DbPassword)' }
        { name: 'SENDGRID_API_KEY', value: '@Microsoft.KeyVault(VaultName=${keyVaultName};SecretName=SendGridApiKey)' }
        { name: 'AZURE_ACCOUNT_KEY', value: '@Microsoft.KeyVault(VaultName=${keyVaultName};SecretName=AzureAccountKey)' }
        // Non-sensitive config
        { name: 'DB_HOST', value: dbHost }
        { name: 'DB_NAME', value: dbName }
        { name: 'DB_USER', value: dbUser }
        { name: 'DB_PORT', value: '1433' }
        { name: 'AZURE_ACCOUNT_NAME', value: azureAccountName }
        { name: 'AZURE_CONTAINER', value: azureContainer }
        { name: 'DISABLE_COLLECTSTATIC', value: '0' }
        { name: 'SCM_DO_BUILD_DURING_DEPLOYMENT', value: 'true' }
      ]
    }
  }
  tags: {
    environment: 'production'
    project: 'hellenvanmeene'
    runtime: 'python'
  }
}

// -------------------------------------------------------------------------
// Custom hostname bindings
// DNS (A record or CNAME + TXT asuid.<hostname>) must be set up first.
// -------------------------------------------------------------------------

resource hostBindings 'Microsoft.Web/sites/hostNameBindings@2023-12-01' = [
  for hostname in customHostnames: {
    parent: webApp
    name: hostname
    properties: {
      siteName: appName
      hostNameType: 'Verified'
    }
  }
]

// -------------------------------------------------------------------------
// Outputs
// -------------------------------------------------------------------------

output webAppId string = webApp.id
output defaultHostname string = webApp.properties.defaultHostName

@description('Add as TXT record (asuid.<hostname>) to verify domain ownership.')
@secure()
output customDomainVerificationId string = webApp.properties.customDomainVerificationId

@description('Outbound IPs (comma-separated). Use the first for DNS A record.')
output outboundIpAddresses string = webApp.properties.outboundIpAddresses

output portalUrl string = 'https://portal.azure.com/#resource${webApp.id}'
output keyVaultUri string = kv.outputs.keyVaultUri
output webAppPrincipalId string = webApp.identity.principalId
