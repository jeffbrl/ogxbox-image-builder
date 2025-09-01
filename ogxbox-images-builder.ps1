param(
    [string]$Size,
    [string]$Output,
    [string]$Czip,
    [string]$Ezip
)

function usage {
    Write-Error "Usage: $PSScriptRoot\script.ps1 -o <output_image> [-s <size_in_GB>] [-c <c_zip_file>] [-e <e_zip_file>]"
    exit 1
}

# Validate mandatory parameters
if (-not $Output) {
    Write-Error "Error: Specifying output image file with -o <file> is mandatory."
    usage
    exit 1
}

$builderArgs = "/data/$Output"

if (-not $Size) {
    Write-Host "Output image size not specified... defaulting to 8GB"
    $Size = 8
}
$builderArgs += " -s $Size"

if ($Czip) {
    $builderArgs += " -c /data/$Czip"
}

if ($Ezip) {
    $builderArgs += " -e /data/$Ezip"
}

# Construct the full Docker command
$dockerCommand = "docker run --rm -v $(Get-Location)/main.py:/app/main.py -v $(Get-Location):/data jeffbrl/ogxbox-image-builder python3 /app/main.py $builderArgs"

# Execute the command
Invoke-Expression $dockerCommand
