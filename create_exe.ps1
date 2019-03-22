# Setup Directory
if (Test-Path dist) {
  Remove-Item dist -Recurse | Out-Null
}
New-Item dist -ItemType Directory | Out-Null
# Search windll.
Write-Host "> Searching WinDLL"
$windll = "c:\windows\WinSxS\x86_microsoft-windows-m..namespace-downlevel_*"
$windllpath = "."
if(Test-Path $windll){
  $item = (Get-ChildItem $windll | Sort-Object LastWriteTime)[0]
  $windllpath = '"c:\windows\WinSxS\{0}"' -f $item.Name
}
# pyinstaller
Write-Host "> Creation EXE"
pyinstaller `
  --onefile `
  --windowed `
  --name RVPreview `
  --icon appicon.ico `
  --path $windllpath `
  --path C:/Windows/System32/downlevel `
  --specpath ./dist/ `
  --distpath ./dist/dist `
  --workpath ./dist/build `
  --add-data "../html;html" `
  --add-data "../node_modules;node_modules" `
  --add-binary "../.venv/Lib/site-packages/webview/lib;webview/lib" `
  --add-binary "../appicon.*;." `
  src\main.py
Write-Host "> Complete"