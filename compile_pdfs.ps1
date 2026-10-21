# CV Builder PDF Compiler - Interactive UI
# Detects folders in _generated/, lets you select one, compiles to PDF, and optionally opens it

$generatedPath = Join-Path $PSScriptRoot "_generated"

# Check if _generated folder exists
if (-not (Test-Path $generatedPath)) {
    Write-Host "❌ Error: _generated folder not found at $generatedPath" -ForegroundColor Red
    exit 1
}

# Get all folders in _generated
$folders = @(Get-ChildItem -Path $generatedPath -Directory -ErrorAction SilentlyContinue | Sort-Object Name)

if ($folders.Count -eq 0) {
    Write-Host "❌ No folders found in _generated/" -ForegroundColor Red
    exit 1
}

# Display header
Write-Host "`n" -NoNewline
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "  CV Builder PDF Compiler" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

# Show menu
Write-Host "Found $($folders.Count) folder(s) to compile:`n" -ForegroundColor White
for ($i = 0; $i -lt $folders.Count; $i++) {
    $folder = $folders[$i]
    $mdCount = (Get-ChildItem -Path $folder.FullName -Filter "*.md" -File).Count
    Write-Host "  $($i+1). $($folder.Name)" -ForegroundColor Green -NoNewline
    Write-Host " ($mdCount markdown file(s))" -ForegroundColor DarkGray
}

Write-Host "`n  0. Exit`n" -ForegroundColor DarkGray

# Get user selection
do {
    [int]$selection = 0
    $validInput = [int]::TryParse((Read-Host "Select folder to compile [0-$($folders.Count)]"), [ref]$selection)

    if (-not $validInput -or $selection -lt 0 -or $selection -gt $folders.Count) {
        Write-Host "  ⚠️  Invalid choice. Please enter a number between 0 and $($folders.Count)" -ForegroundColor Yellow
    }
} until ($validInput -and $selection -ge 0 -and $selection -le $folders.Count)

# Exit if user chose 0
if ($selection -eq 0) {
    Write-Host "Goodbye!`n" -ForegroundColor Cyan
    exit 0
}

$selectedFolder = $folders[$selection - 1]
$folderName = $selectedFolder.Name

# Compile
Write-Host "`nCompiling $folderName..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

$pythonCmd = "python compile_all_pdfs.py `"$folderName`" --force"
Write-Host "Running: $pythonCmd`n" -ForegroundColor DarkGray

# Run compilation and capture output
$output = & python compile_all_pdfs.py "$folderName" --force 2>&1
$exitCode = $LASTEXITCODE

# Show output
Write-Host $output

# Check result
if ($exitCode -eq 0) {
    Write-Host "`n" -NoNewline
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host "  ✓ Compilation succeeded!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Green

    # Find generated PDFs
    $pdfFiles = @(Get-ChildItem -Path $selectedFolder.FullName -Filter "*.pdf" -File)

    if ($pdfFiles.Count -gt 0) {
        Write-Host "Generated file(s):`n" -ForegroundColor White
        for ($i = 0; $i -lt $pdfFiles.Count; $i++) {
            $pdf = $pdfFiles[$i]
            $size = "{0:N2}" -f ($pdf.Length / 1MB)
            Write-Host "  $($i+1). $($pdf.Name) ($($size) MB)" -ForegroundColor Green
        }

        Write-Host "`n  0. Don't open`n" -ForegroundColor DarkGray

        # Ask if user wants to open a PDF
        do {
            [int]$openSelection = 0
            $validInput = [int]::TryParse((Read-Host "Open a PDF? [0-$($pdfFiles.Count)]"), [ref]$openSelection)

            if (-not $validInput -or $openSelection -lt 0 -or $openSelection -gt $pdfFiles.Count) {
                Write-Host "  ⚠️  Invalid choice. Please enter a number between 0 and $($pdfFiles.Count)" -ForegroundColor Yellow
            }
        } until ($validInput -and $openSelection -ge 0 -and $openSelection -le $pdfFiles.Count)

        if ($openSelection -gt 0) {
            $pdfToOpen = $pdfFiles[$openSelection - 1].FullName
            Write-Host "`nOpening $($pdfFiles[$openSelection - 1].Name)..." -ForegroundColor Cyan
            Start-Process $pdfToOpen
        }
    }
} else {
    Write-Host "`n" -NoNewline
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host "  ✗ Compilation failed (exit code: $exitCode)" -ForegroundColor Red
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Red
}

Write-Host ""
