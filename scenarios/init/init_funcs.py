from pathlib import Path
import subprocess
from utils import run


def ensure_git():
    try:
        subprocess.run(
            ["git", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("[+] git is installed")
    except Exception:
        raise EnvironmentError("git is not installed")


def ensure_semgrep():
    try:
        subprocess.run(
            ["semgrep", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("[+] semgrep already installed")
    except Exception:
        print("[+] Installing semgrep...")
        run(["python3", "-m", "pip", "install", "semgrep"])


def git_init_and_commit(path: Path):
    if not (path / ".git").exists():
        run(["git", "init"], cwd=path)

    run(["git", "add", "."], cwd=path)

    # есть ли коммит
    try:
        subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            cwd=path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"[=] already committed: {path}")
        return
    except Exception:
        pass

    run(["git", "commit", "-m", "Initial commit (CTF setup)"], cwd=path)


def init_services(base_dir: Path):
    base_dir = base_dir.expanduser().resolve()

    ensure_git()
    ensure_semgrep()

    for item in base_dir.iterdir():
        if item.is_dir():
            print(f"\n[+] Processing {item}")
            try:
                git_init_and_commit(item)
            except Exception as e:
                print(f"[!] Failed: {item} -> {e}")