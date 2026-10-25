$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression

$packRoot = Join-Path $PSScriptRoot 'pack'
$distRoot = Join-Path $PSScriptRoot 'dist'
$release = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'release.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$archivePath = Join-Path $distRoot $release.archive
$files = @('pack.mcmeta', 'pack.png', 'NOTICE.txt', 'LICENSE.txt', 'assets/minecraft/lang/ja_jp.json')

$metadata = Get-Content -LiteralPath (Join-Path $packRoot 'pack.mcmeta') -Raw -Encoding UTF8 | ConvertFrom-Json
$language = Get-Content -LiteralPath (Join-Path $packRoot 'assets/minecraft/lang/ja_jp.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($metadata.pack.pack_format -ne 34) { throw 'Expected pack format 34 for Minecraft 1.21.1.' }
$actualKeys = @($language.PSObject.Properties.Name)
if ($actualKeys.Count -ne $release.entry_count -or $release.keys.Count -ne $release.entry_count) {
    throw 'Translation count differs from release.json.'
}
if (@(Compare-Object $actualKeys @($release.keys)).Count -ne 0) { throw 'Translation keys differ from release.json.' }
$languagePath = Join-Path $packRoot 'assets/minecraft/lang/ja_jp.json'
if ((Get-FileHash -LiteralPath $languagePath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $release.language_sha256) {
    throw 'Language contents differ from release.json. Refresh release data and validate before packaging.'
}
foreach ($relativePath in $files) {
    if (-not (Test-Path -LiteralPath (Join-Path $packRoot $relativePath) -PathType Leaf)) {
        throw "Missing pack file: $relativePath"
    }
}

[System.IO.Directory]::CreateDirectory($distRoot) | Out-Null
$stream = [System.IO.File]::Open($archivePath, [System.IO.FileMode]::Create)
try {
    $archive = [System.IO.Compression.ZipArchive]::new($stream, [System.IO.Compression.ZipArchiveMode]::Create)
    try {
        foreach ($relativePath in $files) {
            # Explicit names keep ZIP paths portable across operating systems.
            $entry = $archive.CreateEntry($relativePath, [System.IO.Compression.CompressionLevel]::Optimal)
            $entryStream = $entry.Open()
            try {
                $bytes = [System.IO.File]::ReadAllBytes((Join-Path $packRoot $relativePath))
                $entryStream.Write($bytes, 0, $bytes.Length)
            } finally { $entryStream.Dispose() }
        }
    } finally { $archive.Dispose() }
} finally { $stream.Dispose() }

Write-Output "Built $($release.entry_count) translations: $archivePath"
