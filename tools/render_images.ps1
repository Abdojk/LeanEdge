# Re-render the social share card (assets/img/og-image.png) with headless Edge.
# The PNG favicons are made by tools/make_logo.py.
# Run from the repo root:  powershell -ExecutionPolicy Bypass -File tools/render_images.ps1
$ErrorActionPreference = "Stop"
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$root = (Get-Location).Path
$jobs = @(
  @{ page = "tools/render/og-image.html"; w = 1200; h = 630; out = "assets/img/og-image.png" }
)
foreach ($j in $jobs) {
  $userDir = Join-Path $env:TEMP ("le-edge-" + [guid]::NewGuid())
  $url = "file:///" + (Join-Path $root $j.page).Replace('\', '/')
  $out = Join-Path $root $j.out
  $edgeArgs = @("--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                "--default-background-color=00000000", "--user-data-dir=`"$userDir`"",
                "--window-size=$($j.w),$($j.h)", "--screenshot=`"$out`"", "`"$url`"")
  Start-Process -FilePath $edge -ArgumentList $edgeArgs -Wait -NoNewWindow | Out-Null
  Start-Sleep -Milliseconds 500
  Remove-Item -Recurse -Force $userDir -ErrorAction SilentlyContinue
  Write-Host "rendered $($j.out)"
}
