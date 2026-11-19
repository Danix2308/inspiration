---
name: inspiration
description: Daniel's video inspiration library. "/inspiration <link>" processes an Instagram/TikTok/YouTube video and logs it in a dated table; "/inspiration" with no link reads the current work context and recommends which saved videos are useful right now.
---

# /inspiration

Dataset: `~/.claude/inspiration/library.md` (one markdown table, one row per video). Never load anything else to answer; keep replies short.

## Always sync to GitHub

`~/.claude/inspiration` is a clone of the public repo https://github.com/Danix2308/inspiration. **Every time the library changes** (row added in Mode A, GitHub-star rows in Mode B, `Tried?` updated, any manual fix) **or this skill's files change**, immediately run:

`python -P ~/.claude/skills/inspiration/sync_github.py "<short commit message, e.g. Add reel: @handle title>"`

It copies the skill into `skill/`, commits and pushes to `main` — no need to ask Daniel first. Add `· synced to GitHub` to the reply. If it prints `sync failed`, tell Daniel the one-line error; the local save still counts.

## Mode A — a link was given (`/inspiration <url> [optional note]`)

1. Check the URL is not already in the library (grep it). If it is, show its row and stop.
2. Run: `python -P ~/.claude/skills/inspiration/fetch_reel.py "<url>"` — prints compact JSON (posted date, creator, caption, local Whisper transcript). Takes ~30–90 s.
   - If both metadata and transcript fail (private reel / login wall), ask Daniel for one line on what the video shows and use that.
3. Append ONE row to the table:
   - **Saved**: today's full date `YYYY-MM-DD` (from the environment, never guessed).
   - **Type**: `reel` / `video` / `workflow` / `skill` / `issue review` / `github repo` / `other`. Non-video links (GitHub repos, skills, workflows): skip fetch_reel.py; read the page/README briefly (for GitHub: `gh repo view owner/name`) and fill the same columns.
   - **Posted**: the video's upload date `YYYY-MM-DD` (or `?`).
   - **Title**: the `title` field (caption's first line, the reel's visible headline); if empty, write a short descriptive title in [brackets].
   - **Creator**: `@handle` (from `handle`).
   - **What it is**: one sentence, concrete (what is shown/taught).
   - **Key idea**: the single most reusable insight/technique, ≤ 20 words.
   - **Useful for**: which of Daniel's projects/kinds of work it applies to (e.g. landing pages, marketing-ai-workflow, CloudA&D video, agents, Fusion/hardware, speeches). Use plain words he'd say when starting that work — this is what Mode B matches on.
   - **Tags**: 3–6 lowercase keywords.
   - **Tried?**: `no`.
   - **Link**: the URL.
   If Daniel added a note, fold it into "Useful for".
4. Reply with just the new row (rendered as a table) and one line: "Saved — I'll suggest it when you work on <useful for>."

## Mode B — no link (`/inspiration`)

0. Run `python -P ~/.claude/skills/inspiration/new_stars.py`. Empty output = no new GitHub stars → skip straight to step 1 using the existing library. Otherwise add one `github repo` row per printed line (Saved = star date) before continuing.
1. Gather context cheaply: the current conversation's task, the working directory name, and at most the project README/CLAUDE.md first lines. Do not research.
2. Read the library table and pick the 1–5 rows whose "Useful for"/Tags actually fit the current work. Prefer rows with `Tried? = no`.
3. Reply with a short table: Video (link) · Saved · Why it helps *this* task · First step to try it. If nothing fits, say so in one line and list the 3 newest untried videos.
4. If Daniel says he tried one, change its `Tried?` to `yes (YYYY-MM-DD)`.

## Table header (create the file with this if missing)

| Saved | Type | Posted | Title | Creator | What it is | Key idea | Useful for | Tags | Tried? | Link |
|---|---|---|---|---|---|---|---|---|---|---|
