import subprocess


def run(cmd, cwd=None):
    print(f"[+] Running: {' '.join(cmd)} (cwd={cwd})")
    subprocess.run(cmd, cwd=cwd, check=True)