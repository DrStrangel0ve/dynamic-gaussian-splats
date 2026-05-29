#!/usr/bin/env bash
set -euo pipefail

cd 'external/4DGaussians'
mkdir -p output

echo '[1/1] train dnerf_bouncingballs'
python train.py -s 'data/dnerf/bouncingballs' --port 6017 --expname 'dnerf/bouncingballs_smoke' --configs 'arguments/dnerf/bouncingballs.py' --iterations 1000
echo '[1/1] render dnerf_bouncingballs'
python render.py --model_path 'output/dnerf/bouncingballs_smoke' --skip_train --configs 'arguments/dnerf/bouncingballs.py' --iteration 1000
echo '[1/1] metrics dnerf_bouncingballs'
python metrics.py --model_paths 'output/dnerf/bouncingballs_smoke'
