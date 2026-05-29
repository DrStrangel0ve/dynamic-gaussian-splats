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
| 4D splats | Does an explicit temporal representation improve quality? |
| foreground masks | Does separating moving objects make static background reconstruction better? |

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

These outputs set up the next step: training static Splatfacto on the full clip, segmented static Splatfacto on windows, and then a 4D Gaussian method on the same windows.

## Repository Shape

- `configs/dynamic_scene_matrix.json` defines baseline temporal experiments.
- `scripts/make_windows.py` writes reproducible time-window manifests.
- `scripts/build_scene_windows.py` generates window manifests for every catalog scene.
- `results/` is reserved for temporal quality and stability tables.

## License

MIT for code and project scaffolding. Source videos and model assets keep their original licenses.
