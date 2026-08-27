param(
    [Parameter(Mandatory = $true)]
    [string]$OpenRouterKey,

    [string]$Repository = "",

    [string]$Branch = "main",

    [string]$Machine = "basicLinux32gb"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required."
}

if (-not $Repository) {
    $Repository = gh repo view --json nameWithOwner --jq .nameWithOwner
}

if (-not $Repository) {
    throw "Could not determine the GitHub repository. Pass -Repository owner/name."
}

$OpenRouterKey | gh secret set OPENROUTER_API_KEY --app codespaces --repos $Repository
if ($LASTEXITCODE -ne 0) {
    throw "Failed to set the Codespaces secret."
}

Write-Host "Creating a fresh Codespace for $Repository..."
$createArgs = @(
    "codespace", "create",
    "--repo", $Repository,
    "--branch", $Branch,
    "--machine", $Machine,
    "--default-permissions",
    "--idle-timeout", "30m"
)
& gh @createArgs

