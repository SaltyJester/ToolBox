# ExchangeOnlineModule must be version 3 or higher
# Must be using PowerShell version 7 or higher



Import-Module ExchangeOnlineManagement
Connect-ExchangeOnline

Remove-DistributionGroupMember -Identity "[group ID]" -Member "[userID]" -Confirm: $False