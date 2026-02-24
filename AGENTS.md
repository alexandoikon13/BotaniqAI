# BotaniqAI

## Cursor Cloud specific instructions

### Overview

BotaniqAI is a single-service Flask application that uses YOLOv8 for plant detection and OpenAI for description generation. There is no microservice architecture—everything runs in one Python process.

### Running the app

```bash
PYTHONPATH=/workspace python3 run.py
```

The Flask dev server starts on `http://127.0.0.1:5000` with debug mode enabled (hot reload active).

### Running tests

```bash
PYTHONPATH=/workspace python3 -m unittest discover -s tests -p "test_*.py" -v
```

The `tests/` directory lacks `__init__.py`, so `PYTHONPATH` must be set to the workspace root for imports to resolve.

### Key caveats

- **System dependency**: OpenCV requires `libgl1` (installed as `libgl1` on Ubuntu 24.04; the old `libgl1-mesa-glx` package no longer exists).
- **YOLOv8 model weights**: `yolov8n.pt` is committed in the repo root and in `tests/`. The model loads at import time when `app/utils.py` is imported, so the first request or test run incurs ~2-3s of model loading time.
- **External services**: Full upload-to-result flow requires `OPENAI_API_KEY`, `CLOUDCUBE_URL`, `CLOUDCUBE_ACCESS_KEY_ID`, and `CLOUDCUBE_SECRET_ACCESS_KEY` environment variables. Without these, the Flask server still starts and serves the UI, and YOLO inference runs, but the post-inference pipeline (S3 upload + OpenAI description) fails.
- **No linter configured**: The repo has no `flake8`, `pylint`, or `ruff` configuration.
- **`python3` not `python`**: The system provides `python3`; there is no `python` alias.
- **pip scripts path**: pip installs to `~/.local/bin` which may not be on `PATH`. Prefix commands with `PATH="$HOME/.local/bin:$PATH"` or run via `python3 -m <module>`.
