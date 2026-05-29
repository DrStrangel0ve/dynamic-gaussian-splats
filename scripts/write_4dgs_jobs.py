#!/usr/bin/env python3
"""Generate shell jobs for the upstream 4DGaussians benchmark."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=Path("configs/4dgs_benchmark_matrix.json"))
    parser.add_argument("--profile", default="smoke", help="Profile id from run_profiles.")
    parser.add_argument("--upstream-dir", default="external/4DGaussians")
    parser.add_argument("--output-script", type=Path, default=Path("jobs/run_4dgs_benchmark.sh"))
    parser.add_argument("--manifest", type=Path, default=Path("results/4dgs_job_manifest.json"))
    return parser.parse_args()


def load_matrix(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def selected_profile(matrix: dict[str, Any], profile_id: str) -> dict[str, Any]:
    for profile in matrix["run_profiles"]:
        if profile["profile_id"] == profile_id:
            return profile
    raise SystemExit(f"Unknown profile: {profile_id}")


def selected_datasets(matrix: dict[str, Any], profile: dict[str, Any]) -> list[dict[str, Any]]:
    wanted = set(profile["datasets"])
    return [dataset for dataset in matrix["datasets"] if dataset["dataset_id"] in wanted]


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def build_job(dataset: dict[str, Any], profile: dict[str, Any], upstream_dir: str, port: int) -> dict[str, Any]:
    expname = f"{dataset['family']}/{dataset['scene']}_{profile['profile_id']}"
    model_path = f"output/{expname}"
    source = dataset["relative_source"]
    config = dataset["config"]
    iterations = int(profile["iterations"])
    render_iteration = int(profile["render_iteration"])
    return {
        "dataset_id": dataset["dataset_id"],
        "profile_id": profile["profile_id"],
        "source": source,
        "config": config,
        "expname": expname,
        "model_path": model_path,
        "train": f"python train.py -s {shell_quote(source)} --port {port} --expname {shell_quote(expname)} --configs {shell_quote(config)} --iterations {iterations}",
        "render": f"python render.py --model_path {shell_quote(model_path)} --skip_train --configs {shell_quote(config)} --iteration {render_iteration}",
        "metrics": f"python metrics.py --model_paths {shell_quote(model_path)}",
        "upstream_dir": upstream_dir,
    }


def write_script(jobs: list[dict[str, Any]], path: Path, upstream_dir: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        f"cd {shell_quote(upstream_dir)}",
        "mkdir -p output",
        "",
    ]
    for index, job in enumerate(jobs, start=1):
        lines.extend(
            [
                f"echo '[{index}/{len(jobs)}] train {job['dataset_id']}'",
                job["train"],
                f"echo '[{index}/{len(jobs)}] render {job['dataset_id']}'",
                job["render"],
                f"echo '[{index}/{len(jobs)}] metrics {job['dataset_id']}'",
                job["metrics"],
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    matrix = load_matrix(args.matrix)
    profile = selected_profile(matrix, args.profile)
    method = next(method for method in matrix["methods"] if method["method_id"] == "4dgs_upstream")
    jobs = [
        build_job(dataset, profile, args.upstream_dir, int(method["default_port"]) + index)
        for index, dataset in enumerate(selected_datasets(matrix, profile))
    ]
    write_script(jobs, args.output_script, args.upstream_dir)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps({"profile": profile, "jobs": jobs}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"jobs": len(jobs), "script": str(args.output_script), "manifest": str(args.manifest)}, indent=2))


if __name__ == "__main__":
    main()
