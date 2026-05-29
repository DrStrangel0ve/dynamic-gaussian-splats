# 4DGS Benchmark Status

Last updated: 2026-05-29

| Track | Status | Notes |
| --- | --- | --- |
| Static open-video baseline | Seeded | Uses existing Splatfacto NCC results in `results/open_video_full_frame_summary.csv`. |
| Windowed static baseline | Prepared | Time-window manifests exist in `results/windows/`. |
| Upstream 4DGaussians setup | Harness ready | `scripts/setup_4dgaussians.sh` clones upstream and initializes submodules. |
| 4DGS smoke job | Generated | `jobs/run_4dgs_benchmark.sh` targets D-NeRF `bouncingballs` for 1,000 iterations. |
| 4DGS metrics | Waiting for long run | `results/4dgs_metrics_summary.md` is empty until upstream `results.json` files exist. |

The expensive step is still the real 4DGS training run. The repo is now ready for that longer compute pass once the D-NeRF or HyperNeRF dataset is installed in the expected upstream layout.
