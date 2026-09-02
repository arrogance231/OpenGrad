import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def capture(root: Path) -> dict[str, Any]:
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        sha = None
    try:
        dirty = bool(
            subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).strip()
        )
    except (OSError, subprocess.CalledProcessError):
        dirty = None
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "os": platform.platform(),
        "kernel": platform.release(),
        "python": sys.version.split()[0],
        "cpu": platform.processor() or platform.machine(),
        "ram_gb": None,
        "gpu": None,
        "cuda": None,
        "rocm": None,
        "git_sha": sha,
        "git_dirty": dirty,
        "gpu_probe": "not performed by Phase 0.5",
    }


def write_capture(root: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(capture(root), indent=2) + "\n")
    return destination
