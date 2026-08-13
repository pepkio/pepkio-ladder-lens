"""Pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local integration runs (never log keys).
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "tool_id": "ladder-lens",
        "title": "Ladder Lens",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "neb_1kb_single_ladder",
                "input": {
                    "unit": "bp",
                    "fit_model": "semi_log_linear",
                    "ladder_mode": "single",
                    "ladder_name": "NEB 1 kb DNA Ladder",
                    "y_well": 40,
                    "y_front": 400,
                    "ladder_bands": [
                        {"label": "L1", "known_size": 10000, "migration_y": 95},
                        {"label": "L2", "known_size": 3000, "migration_y": 145},
                        {"label": "L3", "known_size": 1000, "migration_y": 210},
                    ],
                    "sample_bands": [
                        {"label": "S1", "migration_y": 228},
                    ],
                },
                "output": {"sample_count": 1},
            },
            {
                "name": "dual_ladder_smile",
                "input": {
                    "unit": "bp",
                    "fit_model": "semi_log_linear",
                    "ladder_mode": "dual",
                    "y_well": 40,
                    "y_front": 400,
                    "ladder_bands": [],
                    "sample_bands": [],
                },
                "output": {"sample_count": 0},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test123",
        "status": "completed",
        "result": {
            "fit": {
                "model": "semi_log_linear",
                "r_squared": 0.995,
            },
            "ladder_points": [
                {"label": "L1", "rf": 0.15, "log10_mw": 4, "known_size": 10000},
            ],
            "samples": [
                {
                    "label": "S1",
                    "estimated_size": 799.0,
                    "estimated_size_display": "799 bp",
                    "rf": 0.52,
                    "status": "ok",
                },
            ],
            "warnings": [],
            "methods_text": "Band sizes were estimated by semi-log linear regression...",
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test123",
        "permalink": "https://tools.pepkio.com/r/run_test123",
    }
