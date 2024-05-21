# ExchangeOnlineModule must be version 3 or higher
# Must be using PowerShell version 7 or higher

# if ($args.Count -eq 0){
#     Write-Host "No arguments were passed"
#     exit 1
# }

# $groups = ConvertFrom-Json -InputObject $args[0]

$test = '{"groups": [{"groupId": "631f5b82-9a75-4f5f-ab47-6d62d80527a6", "userId": "c5bf2864-f362-4d7f-af07-9639e4e8655e"}]}'
$test = ConvertFrom-Json -InputObject $test

Write-Host $test.groups[0].userId

# Import-Module ExchangeOnlineManagement
# Connect-ExchangeOnline

# Remove-DistributionGroupMember -Identity "[group ID]" -Member "[userID]" -Confirm: $False