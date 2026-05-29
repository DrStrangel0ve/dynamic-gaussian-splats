# Project Plan

## Milestone 1: Temporal baselines

- Add window manifests for short, medium, and long clips.
- Train static Splatfacto on the full clip as a control.
- Train Splatfacto on overlapping windows as a segmented-static baseline.
- Record quality per window and transition artifacts between windows.

## Milestone 2: Motion-aware inputs

- Add object masks or optical-flow summaries for dynamic regions.
- Compare background-only reconstruction against all-pixel reconstruction.
- Record COLMAP failures caused by moving objects.

## Milestone 3: 4D experiments

- Add a dynamic Gaussian implementation as a separate method family.
- Track temporal PSNR/SSIM/LPIPS, motion consistency, and render speed.
- Export short interactive demos for successful scenes.
