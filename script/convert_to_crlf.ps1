Get-ChildItem -Filter '*.py' -Recurse | ForEach-Object { (Get-Content -Raw -Encoding UTF8 $_.FullName) -replace "`r?`n|`n", "`r`n" | Set-Content -Encoding UTF8 $_.FullName }
Get-ChildItem -Filter '*.bat' -Recurse | ForEach-Object { (Get-Content -Raw -Encoding UTF8 $_.FullName) -replace "`r?`n|`n", "`r`n" | Set-Content -Encoding UTF8 $_.FullName }
Get-ChildItem -Filter '*.env' -Recurse | ForEach-Object { (Get-Content -Raw -Encoding UTF8 $_.FullName) -replace "`r?`n|`n", "`r`n" | Set-Content -Encoding UTF8 $_.FullName }
