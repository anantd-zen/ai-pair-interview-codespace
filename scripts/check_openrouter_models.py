"""Probe candidate OpenRouter models without printing the API key."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request


DEFAULT_MODELS = [
    "z-ai/glm-5.2:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3.5-lightning:free",
    "qwen/qwen3-coder:free",
]


def probe(model: str, api_key: str) -> dict[str, object]:
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-Title": "AI Pair Interview Model Check",
        },
        data=json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": "Reply with exactly OK."}],
                "max_tokens": 16,
            }
        ).encode("utf-8"),
    )

    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = json.load(response)
            return {
                "model": model,
                "ok": True,
                "http_status": response.status,
                "seconds": round(time.monotonic() - started, 2),
                "served_model": payload.get("model"),
            }
    except urllib.error.HTTPError as error:
        try:
            payload = json.loads(error.read().decode("utf-8"))
            message = payload.get("error", {}).get("message", str(error))
        except (UnicodeDecodeError, json.JSONDecodeError):
            message = str(error)
        return {
            "model": model,
            "ok": False,
            "http_status": error.code,
            "seconds": round(time.monotonic() - started, 2),
            "error": message,
        }
    except (TimeoutError, urllib.error.URLError) as error:
        return {
            "model": model,
            "ok": False,
            "http_status": None,
            "seconds": round(time.monotonic() - started, 2),
            "error": str(error),
        }


def main() -> int:
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("DEFAULT_OPENROUTER_API_KEY")
    if not api_key:
        print("No OpenRouter API key is available.", file=sys.stderr)
        return 2

    models = sys.argv[1:] or DEFAULT_MODELS
    results = [probe(model, api_key) for model in models]
    for result in results:
        print(json.dumps(result, sort_keys=True))
    return 0 if any(result["ok"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())

