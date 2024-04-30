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

    # for each group in groups, get members of group, then filter for user by user Object ID
    $groups | ForEach-Object {
        $groupMembers = Get-MsolGroupMember -GroupObjectId $_.ObjectId | Where-Object {$_.ObjectId -eq $user.ObjectId}

        # if user is part of group, append group object to $memberOf
        if($groupMembers){
            $memberOf += ($_)
        }
    }

    return $memberOf
}

function Remove-Groups {
    param (
        [string]$UPN,
        [object]$Groups
    )

    $user = Get-MsolUser -UserPrincipalName $UPN

    foreach ($group in $Groups) {
        Remove-MsolGroupMember -GroupObjectId $group.ObjectId -GroupMemberType User -GroupMemberObjectId $user.ObjectId
    }
}

#Block-SignIn -UPN $upn
#Reset-Password -UPN $upn
$test = Get-Groups -UPN $upn
Remove-Groups -UPN $upn -Groups $test

# Prevents powershell window from closing automatically
Read-Host "Press Enter to close this window"