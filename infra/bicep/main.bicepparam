// Non-sensitive parameters. Safe to commit.
// Deploy alongside secrets.bicepparam:
//   az deployment group create \
//     --resource-group hellenvanmeene \
//     --parameters main.bicepparam secrets.bicepparam
using './main.bicep'

param location = 'westeurope'
param appServicePlanName = 'hellenvanmeene-linux'
param appName = 'hellenvanmeene-django'
param keyVaultName = 'hellenvanmeene-kv'
param kvSubscriptionId = '3c0a1e74-fe18-4403-ad5d-e6550f162731'
param kvResourceGroupName = 'hellenvanmeene'
param dbName = 'HellenvanMeene'
param azureContainer = 'photos'
param customHostnames = [
  'hellenvanmeene.com'
  'www.hellenvanmeene.com'
  'hellenvanmeene.net'
  'www.hellenvanmeene.net'
  'hellenvanmeene.nl'
  'www.hellenvanmeene.nl'
]

// These sensitive parameters should be supplied via a secrets.bicepparam file or CLI:
//   az deployment group create ... --parameters main.bicepparam secrets.bicepparam
param dbHost = ''
param dbUser = ''
param dbPassword = ''
param azureAccountName = ''
param azureAccountKey = ''
param secretKey = ''
param sendgridApiKey = ''
