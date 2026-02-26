#!/usr/bin/env pwsh
<#
.SYNOPSIS
    One-time setup: create the Azure AD federated credential for OIDC
    and populate GitHub secrets so the CI/CD pipeline can authenticate.

.PARAMETER GitHubRepo
    Full slug of the new GitHub repository, e.g. frankvaneykelen/hellenvanmeene-django

.EXAMPLE
    .\pipelines\init-pipeline.ps1 -GitHubRepo "frankvaneykelen/hellenvanmeene-django"
#>

param(
    [Parameter(Mandatory)]
    [string]$GitHubRepo
)

$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Azure identifiers (from the existing app registration)
# ---------------------------------------------------------------------------
$AppId          = "51925ea6-776e-4339-b2d6-9d8bec4436ac"
$TenantId       = "7daaa223-9279-4a97-b3f4-253eae4093ab"
$SubscriptionId = "3c0a1e74-fe18-4403-ad5d-e6550f162731"

Write-Host "`n=== Creating OIDC federated credential ===" -ForegroundColor Cyan

$credName = ($GitHubRepo -replace "/", "-") + "-main"

$params = @{
    name      = $credName
    issuer    = "https://token.actions.githubusercontent.com"
    subject   = "repo:${GitHubRepo}:ref:refs/heads/main"
    audiences = @("api://AzureADTokenExchange")
} | ConvertTo-Json -Compress

az ad app federated-credential create --id $AppId --parameters $params
Write-Host "Federated credential '$credName' created." -ForegroundColor Green

Write-Host "`n=== Setting GitHub secrets ===" -ForegroundColor Cyan
Write-Host "Requires 'gh' CLI to be installed and authenticated."

gh secret set AZURE_CLIENT_ID       --repo $GitHubRepo --body $AppId
gh secret set AZURE_TENANT_ID       --repo $GitHubRepo --body $TenantId
gh secret set AZURE_SUBSCRIPTION_ID --repo $GitHubRepo --body $SubscriptionId

Write-Host "`nDone. Push to main to trigger the first deployment." -ForegroundColor Green
