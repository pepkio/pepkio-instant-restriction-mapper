"""Integration tests against live Pepkio Tools API (local and production)."""

from __future__ import annotations

import os

import pytest

from pepkio_instant_restriction_mapper import PepkioClient, RestrictionMapperInput

ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY") or os.getenv("PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key available for {env_name} environment")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest_live(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "instant-restriction-mapper"
    assert "Instant Restriction Mapper" in manifest["title"]
    examples = live_client.list_examples()
    assert "eco_single_site" in examples


def test_run_example_live(live_client: PepkioClient):
    inp = live_client.get_example_input("eco_single_site")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    enzymes = result.result.get("all_enzymes")
    assert isinstance(enzymes, list)
    assert len(enzymes) > 0
    assert enzymes[0]["name"] == "EcoRI"


def test_get_run_live(live_client: PepkioClient):
    inp = live_client.get_example_input("eco_single_site")
    run_res = live_client.run(inp)
    assert run_res.run_id

    fetched = live_client.get_run(run_res.run_id)
    assert fetched.run_id == run_res.run_id
    assert fetched.status == "completed"
    assert fetched.result is not None


def test_run_input_model_live(live_client: PepkioClient):
    inp = RestrictionMapperInput(
        sequence="AAAAAAAAAAGAATTCAAAAAAAAAA",
        topology="linear",
        cut_frequency=1,
    )
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert result.result.get("sequence_length") == 26
