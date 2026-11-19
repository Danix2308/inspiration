"""Push the inspiration library (and a copy of this skill) to GitHub.

Repo: https://github.com/Danix2308/inspiration  (local clone = ~/.claude/inspiration)
Usage: python -P ~/.claude/skills/inspiration/sync_github.py "<commit message>"
Prints one line: what was pushed, "nothing to sync", or the error.
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path.home() / ".claude" / "inspiration"
SKILL = Path.home() / ".claude" / "skills" / "inspiration"
REMOTE = "https://github.com/Danix2308/inspiration.git"
SKILL_FILES = ["SKILL.md", "fetch_reel.py", "new_stars.py", "sync_github.py"]
TRAILER = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"


def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"sync failed: git {' '.join(args)}: {(r.stderr or r.stdout).strip()}")
        sys.exit(1)
    return r.stdout.strip()


def main():
    msg = sys.argv[1] if len(sys.argv) > 1 else "Update inspiration library"
    if not (REPO / ".git").exists():
        git("init", "-q", "-b", "main")
        git("remote", "add", "origin", REMOTE)
        git("config", "core.autocrlf", "false")
        git("fetch", "-q", "origin")
        git("reset", "-q", "origin/main")
        git("branch", "-u", "origin/main")
    (REPO / "skill").mkdir(exist_ok=True)
    for f in SKILL_FILES:
        if (SKILL / f).exists():
            shutil.copy2(SKILL / f, REPO / "skill" / f)
    git("add", "-A")
    if not git("status", "--porcelain"):
        print("nothing to sync")
        return
    git("commit", "-q", "-m", f"{msg}\n\n{TRAILER}")
    git("pull", "-q", "--rebase", "origin", "main")
    git("push", "-q", "origin", "HEAD:main")
    print(f"pushed {git('rev-parse', '--short', 'HEAD')}: {msg}")


if __name__ == "__main__":
    main()
