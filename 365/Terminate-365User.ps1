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

function Get-Groups {
    param (
        [string]$UPN
    )

    $user = Get-MsolUser -UserPrincipalName $UPN
    $groups = Get-MsolGroup

    $memberOf = New-Object System.Collections.ArrayList

    $groups | ForEach-Object {
        $groupMembers = Get-MsolGroupMember -GroupObjectId $_.ObjectID | Where-Object {$_.ObjectID -eq $user.ObjectID}

        if($groupMembers){
            #$groupDetails = $_.DisplayName, $_.EmailAddress
            #$memberOf[$_.ObjectID.toString()] = $groupDetails
            
            $groupObject = New-Object PSObject -Property @{
                'ObjectID' = $_.ObjectID
                'DisplayName' = $_.DisplayName
                'EmailAddress' = $_.EmailAddress
            }

            $memberOf.Add($_)
        }
    }

    return $memberOf
}

#Block-SignIn -UPN $upn
#Reset-Password -UPN $upn
$test = Get-Groups -UPN $upn
Write-Host $test

# Prevents powershell window from closing automatically
Read-Host "Press Enter to close this window"