# ExchangeOnlineModule must be version 3 or higher
# Must be using PowerShell version 7 or higher

Import-Module ExchangeOnlineManagement

# $moduleName = "ExchangeOnlineManagement"
# $moduleInstalled = Get-Module -Name $moduleName

# if (-not $moduleInstalled) {
#     Write-Host "ExchangeOnlineManagement is not installed" -ForegroundColor Red
#     Write-Host "Please install the Exchange PowerShell module by running the following command:" -ForegroundColor Yellow
#     Write-Host "Install-Module - Name ExchangeOnlineManagement" -ForegroundColor Green
#     exit 1
# }

# if(-not ($moduleInstalled.Version.Major -ge 3)) {
#     Write-Host "Current ExchangeOnlineManagement has to be version 3 or greater"
#     exit 1
# }

Connect-ExchangeOnline

