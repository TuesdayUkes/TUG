# PowerShell script to create a Windows shortcut for update_timestamps.py
# This creates a shortcut on the desktop that runs the timestamp updater

$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = "$DesktopPath\Update TUG Timestamps.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

# Set the target to the batch file
$TugRepoPath = "C:\repos\TuesdayUkes\TUG"
$Shortcut.TargetPath = "$TugRepoPath\update_timestamps.bat"

# Set the working directory to the TUG repo root
$Shortcut.WorkingDirectory = $TugRepoPath

# Set a description
$Shortcut.Description = "Update v= timestamps in TUG index.html file"

# Set an icon (using the default batch file icon)
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,153"

# Save the shortcut
$Shortcut.Save()

Write-Host "Shortcut created successfully at: $ShortcutPath"
Write-Host "Target: $($Shortcut.TargetPath)"
Write-Host "Working Directory: $($Shortcut.WorkingDirectory)"
