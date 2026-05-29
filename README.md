# Dynamic Gaussian Splats

Dynamic and temporal Gaussian splatting experiments for scenes where a single static reconstruction is the wrong model. This repo starts with video-window planning so moving captures can be split into short temporal units before training or evaluation.

## Workload

- Split source videos into overlapping time windows.
- Train or evaluate one splat representation per window.
- Compare static, segmented-static, and dynamic approaches.
- Track temporal stability, reconstruction quality, and render speed.

## Experiment Types

| Type | Question |
| --- | --- |
| static baseline | How badly does a normal 3DGS model handle motion? |
| sliding windows | Can short static splats approximate a changing scene? |
| 4D splats | Does an explicit temporal representation improve quality on true dynamic datasets? |
| foreground masks | Does separating moving objects make static background reconstruction better? |

## 4DGS Benchmark Track

The repo now has a first-class 4D Gaussian Splatting benchmark harness built around [hustvl/4DGaussians](https://github.com/hustvl/4DGaussians), the CVPR 2024 implementation for real-time dynamic scene rendering.

```bash
bash scripts/setup_4dgaussians.sh
python scripts/write_4dgs_jobs.py --profile smoke
bash jobs/run_4dgs_benchmark.sh
python scripts/collect_4dgs_metrics.py
```

The smoke profile targets D-NeRF `bouncingballs` once the dataset exists under `external/4DGaussians/data/dnerf/bouncingballs`. Longer profiles are defined in `configs/4dgs_benchmark_matrix.json`.

## Quick Start

```bash
python scripts/make_windows.py data/videos/example.mp4 --window-seconds 2 --stride-seconds 1 --output results/example_windows.json
python scripts/build_scene_windows.py --video-root ../open-video-3dgs-zoo/videos --window-seconds 2 --stride-seconds 1
```

The script uses `ffprobe` when available. You can also pass `--duration-seconds` manually.

## Populated Contents

This repo includes dynamic workload manifests for the same three open videos used by the NCC reconstruction benchmark.

- `datasets/open_videos_full.json`: source-scene metadata copied from the Nerfstudio experiment.
- `results/windows/`: per-scene overlapping time-window manifests.
- `results/window_summary.md`: count and duration summary for the generated windows.
- `results/open_video_full_frame_summary.csv`: static Splatfacto NCC baseline metrics for comparison.
- `configs/4dgs_benchmark_matrix.json`: D-NeRF/HyperNeRF-oriented 4DGS benchmark matrix.
- `jobs/run_4dgs_benchmark.sh`: generated upstream train/render/metrics job script.
- `results/4dgs_job_manifest.json`: generated machine-readable job manifest.
- `results/4dgs_metrics_summary.md`: collector output; initially empty until a long 4DGS run completes.
- `results/4dgs_benchmark_status.md`: current status of each benchmark track.

These outputs set up the next step: training static Splatfacto on the full clip, segmented static Splatfacto on windows, and then a 4D Gaussian method on the same windows.

## Repository Shape

- `configs/dynamic_scene_matrix.json` defines baseline temporal experiments.
- `docs/4dgs_benchmark_design.md` explains the benchmark split between open-video static baselines and true 4DGS datasets.
- `scripts/make_windows.py` writes reproducible time-window manifests.
- `scripts/build_scene_windows.py` generates window manifests for every catalog scene.
- `scripts/setup_4dgaussians.sh` clones the upstream 4DGaussians repo and initializes submodules.
- `scripts/write_4dgs_jobs.py` generates benchmark shell jobs.
- `scripts/collect_4dgs_metrics.py` aggregates upstream `results.json` files.
- `results/` is reserved for temporal quality and stability tables.

## License

MIT for code and project scaffolding. Source videos and model assets keep their original licenses.
