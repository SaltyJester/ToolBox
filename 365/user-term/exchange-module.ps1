Import-Module ExchangeOnlineManagement

# ExchangeOnlineModule must be version 3 or higher
# Must be using PowerShell version 7 or higher

if ($args.Count -eq 0){
    Write-Host "No arguments were passed"
    exit 1
}

Connect-ExchangeOnline

$groups = ConvertFrom-Json -InputObject $args[0]

foreach ($group in $groups.value){
    Remove-DistributionGroupMember -Identity group.groupId -Member group.userId -Confirm: $False
}