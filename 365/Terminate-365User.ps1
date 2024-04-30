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

    $userDataBefore = Get-MsolUser -UserPrincipalName $UPN

    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+'
    $password = -join ((Get-Random -Count 16 -InputObject $chars.ToCharArray()))
    
    Set-MsolUserPassword -UserPrincipalName $UPN -ForceChangePassword $False -NewPassword $password

    $userDataAfer = Get-MsolUser -UserPrincipalName $UPN

    # Checking to make sure password was updated
    if($userDataAfer.LastPasswordChangeTimestamp -gt $userDataBefore.LastPasswordChangeTimestamp) {
        Write-Host "Password for $UPN was reset"
    }
    else {
        Write-Host "Unable to reset password for $UPN"
    }
}

Block-SignIn -UPN $upn
Reset-Password -UPN $upn

# Prevents powershell window from closing automatically
Read-Host "Press Enter to close this window"