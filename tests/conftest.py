"""Pytest fixtures for pepkio-instant-restriction-mapper."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

# Load monorepo .env for local/prod integration testing
_monorepo_env = Path(__file__).resolve().parents[3] / ".env"
if _monorepo_env.is_file():
    load_dotenv(_monorepo_env)

_package_env = Path(__file__).resolve().parents[1] / ".env"
if _package_env.is_file():
    load_dotenv(_package_env)


@pytest.fixture
def mock_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "tool_id": "instant-restriction-mapper",
        "title": "Instant Restriction Mapper",
        "description": "Client-side restriction enzyme finder.",
        "execution_mode": "sync",
        "examples": [
            {
                "name": "eco_single_site",
                "input": {
                    "sequence": "AAAAAAAAAAGAATTCAAAAAAAAAA",
                    "topology": "linear",
                    "cut_frequency": 1,
                },
                "output": {"all_enzymes": [{"name": "EcoRI"}]},
            },
            {
                "name": "short_sequence_warning",
                "input": {"sequence": "ATGC"},
                "output": {"warnings": ["Sequence too short"]},
            },
        ],
    }


@pytest.fixture
def mock_run_response() -> dict:
    return {
        "run_id": "run_test_12345",
        "status": "completed",
        "result": {
            "sequence_name": "Untitled",
            "sequence_length": 26,
            "topology": "linear",
            "all_enzymes": [
                {
                    "name": "EcoRI",
                    "recognition": "GAATTC",
                    "cut_count": 1,
                    "positions": [10],
                }
            ],
            "fragment_sizes": [26],
            "warnings": [],
            "metadata": {"filters": {"cut_frequency": 1}},
        },
        "error": None,
        "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_test_12345",
        "permalink": "https://tools.pepkio.com/r/run_test_12345",
    }
