#!/usr/bin/env python3
"""Create overlapping time-window manifests for dynamic 3DGS experiments."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, help="Input video path.")
    parser.add_argument("--window-seconds", type=float, default=2.0, help="Window duration in seconds.")
    parser.add_argument("--stride-seconds", type=float, default=1.0, help="Distance between window starts in seconds.")
    parser.add_argument("--duration-seconds", type=float, default=None, help="Override duration if ffprobe is unavailable.")
    parser.add_argument("--output", type=Path, default=None, help="Output JSON path. Defaults to stdout.")
    return parser.parse_args()


def ffprobe_duration(video: Path) -> float | None:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video),
    ]
    try:
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    try:
        return float(completed.stdout.strip())
    except ValueError:
        return None


def build_windows(duration: float, window_seconds: float, stride_seconds: float) -> list[dict[str, Any]]:
    if duration <= 0:
        raise ValueError("duration must be positive")
    if window_seconds <= 0 or stride_seconds <= 0:
        raise ValueError("window and stride must be positive")

    windows: list[dict[str, Any]] = []
    start = 0.0
    index = 0
    while start < duration:
        end = min(duration, start + window_seconds)
        windows.append(
            {
                "window_id": f"window_{index:04d}",
                "start_seconds": round(start, 6),
                "end_seconds": round(end, 6),
                "duration_seconds": round(end - start, 6),
            }
        )
        if end >= duration:
            break
        start += stride_seconds
        index += 1
    return windows


def main() -> None:
    args = parse_args()
    duration = args.duration_seconds if args.duration_seconds is not None else ffprobe_duration(args.video)
    if duration is None:
        raise SystemExit("Could not determine duration. Install ffprobe or pass --duration-seconds.")

    manifest = {
        "video": str(args.video),
        "duration_seconds": duration,
        "window_seconds": args.window_seconds,
        "stride_seconds": args.stride_seconds,
        "windows": build_windows(duration, args.window_seconds, args.stride_seconds),
    }
    text = json.dumps(manifest, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
