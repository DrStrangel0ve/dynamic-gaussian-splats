#!/usr/bin/env python3
"""Build time-window manifests for every open-video scene."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("datasets/open_videos_full.json"))
    parser.add_argument("--video-root", type=Path, default=Path("../open-video-3dgs-zoo/videos"))
    parser.add_argument("--output-root", type=Path, default=Path("results/windows"))
    parser.add_argument("--summary-prefix", type=Path, default=Path("results/window_summary"))
    parser.add_argument("--window-seconds", type=float, default=2.0)
    parser.add_argument("--stride-seconds", type=float, default=1.0)
    return parser.parse_args()


def video_path(video: dict[str, Any], video_root: Path) -> Path:
    local_path = Path(video["local_path"])
    return video_root / local_path.name


def ffprobe_duration(path: Path) -> float:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return float(completed.stdout.strip())


def build_windows(duration: float, window_seconds: float, stride_seconds: float) -> list[dict[str, Any]]:
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


def write_scene_manifest(video: dict[str, Any], source_video: Path, args: argparse.Namespace) -> dict[str, Any]:
    duration = ffprobe_duration(source_video)
    windows = build_windows(duration, args.window_seconds, args.stride_seconds)
    payload = {
        "scene_id": video["scene_id"],
        "label": video["label"],
        "role": video["role"],
        "source_page": video["source_page"],
        "license": video["license"],
        "video_file": str(source_video),
        "duration_seconds": duration,
        "window_seconds": args.window_seconds,
        "stride_seconds": args.stride_seconds,
        "windows": windows,
    }
    args.output_root.mkdir(parents=True, exist_ok=True)
    output_path = args.output_root / f"{video['scene_id']}_windows.json"
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return {
        "scene_id": video["scene_id"],
        "label": video["label"],
        "duration_seconds": duration,
        "window_seconds": args.window_seconds,
        "stride_seconds": args.stride_seconds,
        "windows": len(windows),
        "manifest": str(output_path),
    }


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, Any]], path: Path) -> None:
    lines = [
        "# Dynamic Window Summary",
        "",
        "| Scene | Duration seconds | Window seconds | Stride seconds | Windows | Manifest |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['scene_id']}` | {row['duration_seconds']:.3f} | {row['window_seconds']:.3f} | {row['stride_seconds']:.3f} | {row['windows']} | `{row['manifest']}` |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    rows = [write_scene_manifest(video, video_path(video, args.video_root), args) for video in manifest["videos"]]
    write_csv(rows, args.summary_prefix.with_suffix(".csv"))
    write_markdown(rows, args.summary_prefix.with_suffix(".md"))
    print(json.dumps({"scenes": len(rows), "summary_prefix": str(args.summary_prefix)}, indent=2))


if __name__ == "__main__":
    main()
