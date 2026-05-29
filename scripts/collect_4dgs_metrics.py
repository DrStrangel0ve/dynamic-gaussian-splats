#!/usr/bin/env python3
"""Collect upstream 4DGaussians results.json files into benchmark tables."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


METRICS = ["PSNR", "SSIM", "LPIPS-vgg", "LPIPS-alex", "MS-SSIM", "D-SSIM"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--upstream-output", type=Path, default=Path("external/4DGaussians/output"))
    parser.add_argument("--summary-prefix", type=Path, default=Path("results/4dgs_metrics_summary"))
    return parser.parse_args()


def read_results(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for method, values in payload.items():
        row: dict[str, Any] = {
            "model_path": str(path.parent),
            "method": method,
        }
        for metric in METRICS:
            row[metric] = values.get(metric)
        rows.append(row)
    return rows


def collect(output_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(output_root.glob("**/results.json")):
        rows.extend(read_results(path))
    return rows


def fmt(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["model_path", "method", *METRICS]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: fmt(row.get(field)) for field in fieldnames})


def write_markdown(rows: list[dict[str, Any]], path: Path) -> None:
    columns = ["model_path", "method", *METRICS]
    lines = [
        "# 4DGS Metrics Summary",
        "",
    ]
    if not rows:
        lines.extend(
            [
                "No upstream `results.json` files were found yet.",
                "",
                "Run `scripts/setup_4dgaussians.sh`, prepare a D-NeRF or HyperNeRF dataset, generate jobs with `scripts/write_4dgs_jobs.py`, then run the generated job script.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "| " + " | ".join(columns) + " |",
                "| " + " | ".join(["---"] * len(columns)) + " |",
            ]
        )
        for row in rows:
            lines.append("| " + " | ".join(fmt(row.get(column)) for column in columns) + " |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    rows = collect(args.upstream_output)
    write_csv(rows, args.summary_prefix.with_suffix(".csv"))
    write_markdown(rows, args.summary_prefix.with_suffix(".md"))
    print(json.dumps({"rows": len(rows), "summary_prefix": str(args.summary_prefix)}, indent=2))


if __name__ == "__main__":
    main()
