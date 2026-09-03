import argparse
import json
from pathlib import Path

from opengrad.data.audit import coverage_report, load_records, render_human
from opengrad.env_capture import capture
from opengrad.registry.preflight import check
from opengrad.registry.validate import validate


def preflight(root: Path) -> int:
    checks = [*check(root).items(), ("Environment capture", bool(capture(root).get("python")))]
    print("OpenGrad Pre-Experiment Readiness\n")
    for name, ok in checks:
        print(f"{name:<24} {'PASS' if ok else 'FAIL'}")
    print("\nGPU experiments: NOT STARTED")
    if all(ok for _, ok in checks):
        print("\nREADY_FOR_PHASE_1")
    else:
        print("\nNOT_READY_FOR_PHASE_1")
    return 0 if all(ok for _, ok in checks) else 1


def data_audit_cli() -> int:
    parser = argparse.ArgumentParser(prog="opengrad-data-audit")
    parser.add_argument("--records", required=True, help="JSON array or JSONL canonical records")
    parser.add_argument("--config", help="mixture config retained for audit provenance")
    parser.add_argument("--json", action="store_true", help="also emit machine-readable JSON")
    args = parser.parse_args()
    report = coverage_report(load_records(Path(args.records)))
    print(render_human(report))
    if args.json:
        print("\nJSON_REPORT")
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="opengrad")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("validate")
    sub.add_parser("preflight")
    data_audit = sub.add_parser("data-audit")
    data_audit.add_argument(
        "--records", required=True, help="JSON array or JSONL canonical records"
    )
    data_audit.add_argument("--config", help="mixture config retained for audit provenance")
    data_audit.add_argument("--json", action="store_true", help="also emit machine-readable JSON")
    env = sub.add_parser("env")
    env.add_subparsers(dest="env_command").add_parser("capture")
    args = parser.parse_args()
    root = Path.cwd()
    if args.command == "validate":
        errors = validate(root)
        print("OK" if not errors else "\n".join(errors))
        return int(bool(errors))
    if args.command == "preflight":
        return preflight(root)
    if args.command == "data-audit":
        report = coverage_report(load_records(Path(args.records)))
        print(render_human(report))
        if args.json:
            print("\nJSON_REPORT")
            print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if args.command == "env" and args.env_command == "capture":
        print(capture(root))
        return 0
    parser.print_help()
    return 0


def preflight_cli() -> int:
    return preflight(Path.cwd())
