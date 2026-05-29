# Dynamic 4DGS Benchmark Design

This project now separates two related workloads:

- Static and windowed static Gaussian splats for monocular open videos.
- True dynamic 4D Gaussian Splatting using datasets that match the upstream 4DGaussians layouts.

The upstream 4DGaussians project is the baseline method for the second workload. Its README describes D-NeRF, HyperNeRF, DyNeRF, and multiple-view data layouts, plus training with `train.py`, rendering with `render.py`, and metric evaluation with `metrics.py`.

## Benchmark Stages

| Stage | Method | Dataset | Purpose |
| --- | --- | --- | --- |
| Static baseline | Nerfstudio Splatfacto | open videos | Measures how a static splat handles motion or temporal redundancy. |
| Windowed static | Nerfstudio Splatfacto per window | open videos | Measures whether short static windows are enough for mild motion. |
| 4DGS smoke | 4DGaussians | D-NeRF `bouncingballs` | Verifies CUDA, submodules, training, render, and metric collection. |
| 4DGS sweep | 4DGaussians | D-NeRF and HyperNeRF | Long-running quality/runtime comparison for dynamic scenes. |

## Why Not Train 4DGS Directly On The Three Open Videos?

The open videos in this workspace are single monocular videos selected for reconstruction experiments. They are useful for static and windowed-static comparisons, but they are not automatically valid multi-view dynamic datasets. 4DGaussians expects structured dynamic scene data such as D-NeRF, HyperNeRF, DyNeRF, or multiple synchronized camera folders. The harness therefore keeps the open videos as static baselines and uses D-NeRF/HyperNeRF-style scenes as the real 4DGS baseline.

## Outputs

- `jobs/run_4dgs_benchmark.sh`: generated train/render/metric commands.
- `results/4dgs_job_manifest.json`: machine-readable job list.
- `results/4dgs_metrics_summary.csv`: aggregate metrics collected from upstream `results.json` files.
- `results/4dgs_metrics_summary.md`: readable benchmark table.

## Suggested Long Runs

1. Run `smoke` on `dnerf_bouncingballs` to validate the environment.
2. Run `paperish_dnerf` on the D-NeRF scenes once smoke succeeds.
3. Add HyperNeRF scenes only after COLMAP/precomputed point-cloud paths are stable.
4. Keep static and windowed-static metrics in the same final report so the portfolio shows why temporal modeling matters.
