<#
Modules Needed:
Connect-MsolService
#>

$upn = Read-Host "Please enter UPN of user to be terminated"

Connect-MsolService

function Block-SignIn {
    param (
        [string]$UPN
    )

    Set-MsolUser -UserPrincipalName $UPN -BlockCredential $True

    # Checking to make sure user's sign was indeed blocked
    $user = Get-MsolUser -UserPrincipalName $upn
    $displayName = $user.DisplayName
    if($user.BlockCredential) {
        Write-Host "Sign in for $UPN was blocked"
    }
    else {
        Write-Host "Unable to block sign in for $UPN"
    }
}

function Reset-Password {
    param (
        [string]$UPN
    )


}

Block-SignIn -UPN $upn

# Prevents powershell window from closing automatically
Read-Host "Press Enter to close this window"