param(
    [string]$OpenRouterKey = "",

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

if ($OpenRouterKey) {
    $OpenRouterKey | gh secret set OPENROUTER_API_KEY --app codespaces --repos $Repository
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to set the per-interview Codespaces secret."
    }
    Write-Host "Using the supplied per-interview OpenRouter override."
} else {
    Write-Host "Using the repository's DEFAULT_OPENROUTER_API_KEY Codespaces secret."
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

