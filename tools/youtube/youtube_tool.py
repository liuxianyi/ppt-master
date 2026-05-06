#!/usr/bin/env python3
"""
Lightweight wrapper around yt-dlp / youtube-dl for common download tasks.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download YouTube content as mp4 or mp3."
    )
    parser.add_argument("url", help="YouTube video or playlist URL")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="downloads",
        help="Directory for downloaded files (default: downloads)",
    )
    parser.add_argument(
        "--audio-only",
        action="store_true",
        help="Download audio only and extract as mp3",
    )
    parser.add_argument(
        "--list-formats",
        action="store_true",
        help="List available formats instead of downloading",
    )
    parser.add_argument(
        "--write-info-json",
        action="store_true",
        help="Write metadata json next to the download",
    )
    parser.add_argument(
        "--write-thumbnail",
        action="store_true",
        help="Write thumbnail image next to the download",
    )
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="Print the resolved downloader command before running it",
    )
    return parser


def resolve_downloader() -> str:
    for candidate in ("yt-dlp", "youtube-dl"):
        binary = shutil.which(candidate)
        if binary:
            return binary

    raise SystemExit(
        "No supported downloader found in PATH.\n"
        "Install yt-dlp first (recommended):\n"
        "  brew install yt-dlp\n"
        "or:\n"
        "  python3 -m pip install --upgrade yt-dlp\n"
        "\nFallback option:\n"
        "  brew install youtube-dl\n"
        "or:\n"
        "  python3 -m pip install --upgrade youtube-dl"
    )


def normalize_url(raw_url: str) -> str:
    url = raw_url.strip().strip("`").strip().strip("\"'").strip()
    parsed = urlparse(url)

    if "youtube.com" in parsed.netloc and parsed.path.startswith("/shorts/"):
        video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    if "youtu.be" in parsed.netloc:
        video_id = parsed.path.lstrip("/").split("/", 1)[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    if "youtube.com" in parsed.netloc and parsed.path == "/watch":
        video_id = parse_qs(parsed.query).get("v", [""])[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    return re.sub(r"\s+", "", url)


def build_command(args: argparse.Namespace, downloader_bin: str) -> list[str]:
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    url = normalize_url(args.url)
    template = str(output_dir / "%(upload_date)s_%(title)s_%(id)s.%(ext)s")
    command = [downloader_bin, "-o", template]

    if args.audio_only:
        command.extend(["-x", "--audio-format", "mp3"])
    else:
        # Prefer a directly downloadable mp4 stream first to reduce ffmpeg reliance.
        command.extend(
            [
                "-f",
                "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
                "--merge-output-format",
                "mp4",
            ]
        )

    if args.list_formats:
        command.append("-F")

    if args.write_info_json:
        command.append("--write-info-json")

    if args.write_thumbnail:
        command.append("--write-thumbnail")

    command.append(url)
    return command


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    downloader_bin = resolve_downloader()
    command = build_command(args, downloader_bin)

    if args.print_command:
        print("Resolved command:")
        print(" ".join(command))

    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
