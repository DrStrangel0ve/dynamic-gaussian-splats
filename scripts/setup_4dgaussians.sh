#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_URL="${UPSTREAM_URL:-https://github.com/hustvl/4DGaussians.git}"
UPSTREAM_DIR="${UPSTREAM_DIR:-external/4DGaussians}"
ENV_NAME="${ENV_NAME:-Gaussians4D}"
PYTHON_VERSION="${PYTHON_VERSION:-3.7}"

mkdir -p "$(dirname "$UPSTREAM_DIR")"

if [[ ! -d "$UPSTREAM_DIR/.git" ]]; then
  git clone "$UPSTREAM_URL" "$UPSTREAM_DIR"
else
  git -C "$UPSTREAM_DIR" fetch --all --tags
fi

git -C "$UPSTREAM_DIR" submodule update --init --recursive

cat <<EOF
4DGaussians source is ready at: $UPSTREAM_DIR

Recommended environment, matching upstream guidance:

  conda create -n $ENV_NAME python=$PYTHON_VERSION -y
  conda activate $ENV_NAME
  cd $UPSTREAM_DIR
  pip install -r requirements.txt
  pip install -e submodules/depth-diff-gaussian-rasterization
  pip install -e submodules/simple-knn

The upstream README notes PyTorch 1.13.1 + CUDA 11.6 in their environment.
After installing datasets, generate jobs with:

  python scripts/write_4dgs_jobs.py --profile smoke

EOF
