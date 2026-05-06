#!/usr/bin/env python3
"""
Convert legacy .doc files to .docx, then to Markdown via PPT Master's doc_to_md.py.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DOC_TO_MD = REPO_ROOT / "skills" / "ppt-master" / "scripts" / "source_to_md" / "doc_to_md.py"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert .doc/.docx files to Markdown.",
    )
    parser.add_argument("input", help="Input .doc or .docx file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output Markdown file path (default: alongside input)",
    )
    parser.add_argument(
        "--docx-output",
        help="Path for intermediate .docx output when input is .doc",
    )
    parser.add_argument(
        "--keep-docx",
        action="store_true",
        help="Keep the intermediate .docx file when input is .doc",
    )
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="Print resolved subprocess commands before running",
    )
    return parser


def run_command(command: list[str], print_command: bool) -> None:
    if print_command:
        print("Resolved command:")
        print(" ".join(command))
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def resolve_converter() -> str | None:
    for candidate in ("soffice", "libreoffice", "pandoc"):
        binary = shutil.which(candidate)
        if binary:
            return binary
    return None


def convert_doc_to_docx(
    input_file: Path,
    docx_output: Path,
    print_command: bool,
) -> Path:
    converter = resolve_converter()
    if not converter:
        raise SystemExit(
            "No .doc converter found in PATH.\n"
            "Install one of the following:\n"
            "  brew install --cask libreoffice\n"
            "or:\n"
            "  brew install pandoc"
        )

    docx_output.parent.mkdir(parents=True, exist_ok=True)

    if Path(converter).name in ("soffice", "libreoffice"):
        outdir = docx_output.parent
        command = [
            converter,
            "--headless",
            "--convert-to",
            "docx",
            "--outdir",
            str(outdir),
            str(input_file),
        ]
        run_command(command, print_command)

        converted = outdir / f"{input_file.stem}.docx"
        if not converted.exists():
            raise SystemExit("LibreOffice conversion reported success but no .docx was created.")
        if converted.resolve() != docx_output.resolve():
            shutil.move(str(converted), str(docx_output))
        return docx_output

    command = [
        converter,
        str(input_file),
        "-o",
        str(docx_output),
    ]
    run_command(command, print_command)
    if not docx_output.exists():
        raise SystemExit("Pandoc conversion reported success but no .docx was created.")
    return docx_output


def convert_docx_to_md(
    input_file: Path,
    output_file: Path | None,
    print_command: bool,
) -> None:
    command = [sys.executable, str(DOC_TO_MD), str(input_file)]
    if output_file is not None:
        command.extend(["-o", str(output_file)])
    run_command(command, print_command)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_file = Path(args.input).expanduser().resolve()
    if not input_file.exists():
        raise SystemExit(f"Input file not found: {input_file}")

    suffix = input_file.suffix.lower()
    if suffix not in (".doc", ".docx"):
        raise SystemExit("Only .doc and .docx are supported.")

    output_file = Path(args.output).expanduser().resolve() if args.output else None

    intermediate_docx: Path | None = None
    source_for_md = input_file

    if suffix == ".doc":
        intermediate_docx = (
            Path(args.docx_output).expanduser().resolve()
            if args.docx_output
            else input_file.with_suffix(".docx")
        )
        print(f"[INFO] Converting legacy .doc to .docx: {input_file.name}")
        source_for_md = convert_doc_to_docx(
            input_file=input_file,
            docx_output=intermediate_docx,
            print_command=args.print_command,
        )

    print(f"[INFO] Converting to Markdown via PPT Master: {source_for_md.name}")
    convert_docx_to_md(
        input_file=source_for_md,
        output_file=output_file,
        print_command=args.print_command,
    )

    if intermediate_docx and not args.keep_docx and intermediate_docx.exists():
        intermediate_docx.unlink()
        print(f"[INFO] Removed intermediate file: {intermediate_docx}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
