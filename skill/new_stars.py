"""Cheap check: print ONLY GitHub starred repos not yet in the library (one TSV line each).
Prints nothing when there are no new stars -> /inspiration just uses the existing library.
Usage: python -P new_stars.py
"""
import os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
lib = open(os.path.expanduser("~/.claude/inspiration/library.md"), encoding="utf-8").read().lower()
r = subprocess.run(
    ["gh", "api", "user/starred", "--paginate", "-H", "Accept: application/vnd.github.star+json",
     "--jq", '.[] | [.starred_at[:10], .repo.full_name, (.repo.description // "" | .[:160]), .repo.html_url] | @tsv'],
    capture_output=True, text=True, encoding="utf-8")
if r.returncode:
    print("gh error:", r.stderr.strip()[:200]); sys.exit(1)
for line in r.stdout.splitlines():
    url = line.split("\t")[-1]
    if url.lower() not in lib:
        print(line)
