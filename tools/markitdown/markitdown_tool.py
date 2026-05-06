#!/usr/bin/env python3
"""
Lightweight wrapper for converting local documents to Markdown with MarkItDown.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LOCAL_MARKITDOWN_SRC = REPO_ROOT / "markitdown" / "packages" / "markitdown" / "src"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a local file to Markdown with MarkItDown.",
    )
    parser.add_argument("input", help="Input file path")
    parser.add_argument(
        "-o",
        "--output",
        help="Output Markdown file path (default: next to input with .md extension)",
    )
    parser.add_argument(
        "-x",
        "--extension",
        help="Optional extension hint for MarkItDown, useful for stdin-like flows",
    )
    parser.add_argument(
        "-m",
        "--mime-type",
        help="Optional MIME type hint passed to MarkItDown",
    )
    parser.add_argument(
        "-c",
        "--charset",
        help="Optional charset hint passed to MarkItDown",
    )
    parser.add_argument(
        "--use-plugins",
        action="store_true",
        help="Enable MarkItDown plugins if they are installed",
    )
    parser.add_argument(
        "--install-missing",
        action="store_true",
        help="Install MarkItDown from PyPI if no local or installed runtime is found",
    )
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="Print the resolved MarkItDown command before running",
    )
    return parser


def derive_output_path(input_file: Path, output: str | None) -> Path:
    if output:
        return Path(output).expanduser().resolve()
    return input_file.with_suffix(".md")


def resolve_markitdown_runtime(
    install_missing: bool,
) -> tuple[list[str], dict[str, str] | None]:
    binary = shutil.which("markitdown")
    if binary:
        return [binary], None

    if LOCAL_MARKITDOWN_SRC.exists():
        env = os.environ.copy()
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = (
            f"{LOCAL_MARKITDOWN_SRC}{os.pathsep}{existing}"
            if existing
            else str(LOCAL_MARKITDOWN_SRC)
        )
        return [sys.executable, "-m", "markitdown"], env

    if install_missing:
        install_command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "markitdown[all]",
        ]
        completed = subprocess.run(install_command, check=False)
        if completed.returncode != 0:
            raise SystemExit(completed.returncode)

        binary = shutil.which("markitdown")
        if binary:
            return [binary], None

    raise SystemExit(
        "MarkItDown is not available.\n"
        "Options:\n"
        "  1. Use the bundled source checkout in this repo\n"
        "  2. Install it manually:\n"
        "     python3 -m pip install \"markitdown[all]\"\n"
        "  3. Re-run this tool with --install-missing"
    )


def build_command(
    runtime_cmd: list[str],
    input_file: Path,
    output_file: Path,
    args: argparse.Namespace,
) -> list[str]:
    command = [*runtime_cmd, str(input_file), "-o", str(output_file)]

    if args.extension:
        command.extend(["-x", args.extension])
    if args.mime_type:
        command.extend(["-m", args.mime_type])
    if args.charset:
        command.extend(["-c", args.charset])
    if args.use_plugins:
        command.append("--use-plugins")

    return command


def verify_output(output_file: Path) -> None:
    if not output_file.exists():
        raise SystemExit(f"Conversion finished but output file was not created: {output_file}")

    if output_file.stat().st_size == 0:
        raise SystemExit(f"Conversion finished but output file is empty: {output_file}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_file = Path(args.input).expanduser().resolve()
    if not input_file.exists():
        raise SystemExit(f"Input file not found: {input_file}")
    if not input_file.is_file():
        raise SystemExit(f"Input path is not a file: {input_file}")

    output_file = derive_output_path(input_file, args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    runtime_cmd, env = resolve_markitdown_runtime(args.install_missing)
    command = build_command(runtime_cmd, input_file, output_file, args)

    if args.print_command:
        print("Resolved command:")
        print(" ".join(command))

    completed = subprocess.run(command, check=False, env=env)
    if completed.returncode != 0:
        return completed.returncode

    verify_output(output_file)
    print(f"[INFO] Converted: {input_file}")
    print(f"[INFO] Output: {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
