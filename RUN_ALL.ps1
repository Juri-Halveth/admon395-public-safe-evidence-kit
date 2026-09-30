$ErrorActionPreference = "Stop"

Write-Host "[1/3] Verify package"
py scripts\verify_package.py

Write-Host "[2/3] Analyze HTML"
$env:PYTHONIOENCODING = "utf-8"
py scripts\analyze_admon_html.py | Out-File -Encoding utf8 analysis.page1.json

Write-Host "[3/3] Rebuild PDF"
py scripts\build_admon395_pdf.py

Write-Host "DONE"

