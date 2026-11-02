#!/usr/bin/env bash
# Installs the exact toolchain HW3 is checked with.
#
# This ONE script is used in every place your code runs, so that all of them
# see identical tool versions (and therefore identical lint/type/test output):
#
#   1. .devcontainer/Dockerfile   -> the image you develop in (Codespaces / Docker)
#   2. .github/workflows/ci.yml   -> runs inside that same image
#   3. the Gradescope autograder  -> runs this script in its setup step
#
# Must run as root on Ubuntu 22.04 (x86_64 or arm64).
# Python packages (pytest, ruff, mutmut, hypothesis, ...) are NOT installed here: they are
# pinned in uv.lock and installed into /opt/uv/venv by the Dockerfile (or the
# autograder's setup.sh). uv is only used to build the environment; students
# don't need to run it.
set -euo pipefail

UV_VERSION="0.9.28"
PYTHON_VERSION="3.11"

# Where uv keeps its Python, cache, and the virtualenv. The virtualenv lives
# OUTSIDE the repo, so nothing from your own laptop can collide with it.
# Keep these in sync with the ENV lines in .devcontainer/Dockerfile.
export UV_PYTHON_INSTALL_DIR=/opt/uv/python
export UV_CACHE_DIR=/opt/uv/cache
export UV_PROJECT_ENVIRONMENT=/opt/uv/venv
export UV_LINK_MODE=copy

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
    ca-certificates curl git make unzip
rm -rf /var/lib/apt/lists/*

# uv (installs a single static binary into /usr/local/bin)
curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" \
    | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh

# Python, managed by uv so the version doesn't depend on the OS
mkdir -p /opt/uv
uv python install "${PYTHON_VERSION}"

# Anyone (the `vscode` user in the dev container, root in CI/Gradescope) may use /opt/uv
chmod -R a+rwX /opt/uv

echo "Installed: $(uv --version), $(make --version | head -1)"
