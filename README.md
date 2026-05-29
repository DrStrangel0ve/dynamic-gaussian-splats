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
```

The script uses `ffprobe` when available. You can also pass `--duration-seconds` manually.

## Repository Shape

- `configs/dynamic_scene_matrix.json` defines baseline temporal experiments.
- `scripts/make_windows.py` writes reproducible time-window manifests.
- `results/` is reserved for temporal quality and stability tables.

## License

MIT for code and project scaffolding. Source videos and model assets keep their original licenses.
