from pathlib import Path
from utils import run, sarif_to_html
from datetime import datetime
import subprocess


RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")

REPORTS_DIR = Path.cwd() / "reports" / RUN_ID

BASE_DIR = Path(__file__).resolve().parents[0]

SEMGREP_RULES_DIR = BASE_DIR / "semgrep_rules"


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


def collect_rules(rules_dir: Path):
    if not rules_dir.exists():
        raise FileNotFoundError(rules_dir)

    rules = list(rules_dir.rglob("*.yaml"))

    if not rules:
        raise ValueError(f"No semgrep rules found in {rules_dir}")

    return rules


def scan_semgrep(target: Path, report_path: Path):
    target = target.expanduser().resolve()

    if not target.exists():
        raise FileNotFoundError(target)

    report_path.parent.mkdir(parents=True, exist_ok=True)

    rules = collect_rules(SEMGREP_RULES_DIR)

    cmd = [
        "semgrep",
        "scan",
        "--sarif",
        "--output",
        str(report_path),
    ]

    # add all local rules
    for rule in rules:
        cmd += ["--config", str(rule)]

    cmd += ["."]

    print(f"[+] Starting semgrep scan: {target}")
    print(f"[+] Using rules: {len(rules)}")
    print(f"[+] SARIF report: {report_path}")

    run(cmd, cwd=target)

    print(f"[+] Finished semgrep scan: {target}")



def sast_scan(base_dir: Path):
    base_dir = base_dir.expanduser().resolve()

    if not base_dir.exists():
        raise FileNotFoundError(base_dir)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    rules = collect_rules(SEMGREP_RULES_DIR)
    print(f"[+] Loaded rules: {len(rules)}")

    for item in base_dir.iterdir():

        if item.is_dir():

            print(f"\n[+] Processing {item}")

            try:
                sarif_file = REPORTS_DIR / f"{item.name}.sarif"
                html_file = REPORTS_DIR / f"{item.name}.html"
                
                # 1. ensure semgrep
                ensure_semgrep()

                # 1. scan
                scan_semgrep(item, sarif_file)

                # 2. convert SARIF → HTML
                sarif_to_html(sarif_file, html_file)

                # 3. cleanup SARIF (leave only pretty report)
                sarif_file.unlink(missing_ok=True)

                print(f"[+] Clean report ready: {html_file}")

            except Exception as e:
                print(f"[!] Failed: {item} -> {e}")