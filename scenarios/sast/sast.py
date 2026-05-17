from pathlib import Path
from utils import run

SEMGREP_RULES_BASE_DIR = Path(__file__).resolve().parents[0]

SEMGREP_CONFIGS = [
    f"{SEMGREP_RULES_BASE_DIR}/semgrep_rules/misconf.yaml",
]


def scan_semgrep(target: Path):
    target = target.expanduser().resolve()

    if not target.exists():
        raise FileNotFoundError(target)

    cmd = ["semgrep", "scan"]

    for config in SEMGREP_CONFIGS:
        cmd.extend(["--config", config])

    cmd.append(".")

    print(f"[+] Starting semgrep scan: {target}")

    run(cmd, cwd=target)

    print(f"[+] Finished semgrep scan: {target}")


def sast_scan(base_dir: Path):
    base_dir = base_dir.expanduser().resolve()

    if not base_dir.exists():
        raise FileNotFoundError(base_dir)

    for item in base_dir.iterdir():
        if item.is_dir():
            print(f"\n[+] Processing {item}")

            try:
                scan_semgrep(item)

            except Exception as e:
                print(f"[!] Failed: {item} -> {e}")