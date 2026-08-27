# Exporting and reviewing Pi sessions

Pi saves sessions automatically inside the ignored `.interview-work/pi-agent/`
directory for the lifetime of the Codespace.

## During the interview

Name the session inside Pi:

```text
/name candidate-role-date
```

Use `/session` to inspect the current session ID, path, message counts, token
usage, and cost information.

## Export before closing Pi

When Pi is running from `challenge/`:

```text
/export ../.interview-work/review/candidate-role-date.html
```

## Export after Pi exits

From the repository root:

```bash
./scripts/export_latest_session.sh candidate-role-date
```

The helper finds the newest saved JSONL session and exports it to
`.interview-work/review/`.

## Retrieve the HTML

- Locate the file in VS Code Explorer and choose **Download**; or
- copy it from the Codespace with GitHub CLI tooling.

Do not use Pi's `/share` command unless your organization has approved uploading
the session as a private GitHub gist.

## Review and retention

Session HTML can contain candidate prompts, model responses, tool calls, code,
and command output. Tell candidates what is retained, restrict access, define a
retention period, and delete exports that are no longer required.

