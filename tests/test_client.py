"""Unit tests for PepkioClient and CLI (mocked HTTP)."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from click.testing import CliRunner

from pepkio_instant_restriction_mapper.cli import main
from pepkio_instant_restriction_mapper.client import PepkioClient
from pepkio_instant_restriction_mapper.config import (
    DEFAULT_API_BASE_URL,
    resolve_api_key,
    resolve_base_url,
)
from pepkio_instant_restriction_mapper.exceptions import PepkioAPIError
from pepkio_instant_restriction_mapper.models import RestrictionMapperInput, RunResult


def test_config_resolution(monkeypatch: pytest.MonkeyPatch):
    assert resolve_base_url(None) == DEFAULT_API_BASE_URL
    assert resolve_base_url("https://custom.api.com/") == "https://custom.api.com"

    monkeypatch.setenv("PEPKIO_API_BASE_URL", "https://tools.localtest.me")
    assert resolve_base_url(None) == "https://tools.localtest.me"

    monkeypatch.setenv("LOCAL_PEPKIO_API_KEY", "local_key_123")
    assert resolve_api_key(base_url="https://tools.localtest.me") == "local_key_123"

    monkeypatch.setenv("PEPKIO_API_KEY", "prod_key_456")
    assert resolve_api_key(base_url="https://tools.pepkio.com") == "prod_key_456"


def test_get_manifest_mocked(mock_manifest: dict):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/instant-restriction-mapper/manifest"
        return httpx.Response(200, json=mock_manifest)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test_key")
    client._http = httpx.Client(
        base_url=client.base_url, headers=client._http.headers, transport=transport
    )

    manifest = client.get_manifest()
    assert manifest["tool_id"] == "instant-restriction-mapper"

    examples = client.list_examples()
    assert examples == ["eco_single_site", "short_sequence_warning"]

    inp = client.get_example_input("eco_single_site")
    assert inp["sequence"] == "AAAAAAAAAAGAATTCAAAAAAAAAA"


def test_run_mocked(mock_run_response: dict):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/tools/instant-restriction-mapper/run"
        assert request.headers["authorization"] == "Bearer test_key"
        body = json.loads(request.content)
        assert body["input"]["sequence"] == "AAAAAAAAAAGAATTCAAAAAAAAAA"
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test_key")
    client._http = httpx.Client(
        base_url=client.base_url, headers=client._http.headers, transport=transport
    )

    inp = RestrictionMapperInput(
        sequence="AAAAAAAAAAGAATTCAAAAAAAAAA", topology="linear", cut_frequency=1
    )
    res = client.run(inp)
    assert isinstance(res, RunResult)
    assert res.status == "completed"
    assert res.run_id == "run_test_12345"
    assert res.result["all_enzymes"][0]["name"] == "EcoRI"


def test_get_run_mocked(mock_run_response: dict):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tools/v1/runs/run_test_12345"
        return httpx.Response(200, json=mock_run_response)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test_key")
    client._http = httpx.Client(
        base_url=client.base_url, headers=client._http.headers, transport=transport
    )

    res = client.get_run("run_test_12345")
    assert res.status == "completed"


def test_error_handling():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid input sequence",
                }
            },
        )

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test_key")
    client._http = httpx.Client(base_url=client.base_url, transport=transport)

    with pytest.raises(PepkioAPIError) as exc_info:
        client.run({"sequence": ""})
    assert exc_info.value.status_code == 400
    assert exc_info.value.code == "VALIDATION_ERROR"
    assert "Invalid input sequence" in exc_info.value.message


def test_cli_manifest(mock_manifest: dict, monkeypatch: pytest.MonkeyPatch):
    runner = CliRunner()

    def mock_get_manifest(self, *, refresh: bool = False) -> dict[str, Any]:
        return mock_manifest

    monkeypatch.setattr(PepkioClient, "get_manifest", mock_get_manifest)

    res = runner.invoke(main, ["manifest"])
    assert res.exit_code == 0
    assert "Instant Restriction Mapper" in res.output

    res_ex = runner.invoke(main, ["manifest", "--examples"])
    assert res_ex.exit_code == 0
    assert "eco_single_site" in res_ex.output


def test_cli_run(mock_run_response: dict, monkeypatch: pytest.MonkeyPatch):
    runner = CliRunner()

    def mock_run(self, input: Any, **options: Any) -> RunResult:
        return RunResult.model_validate(mock_run_response)

    monkeypatch.setattr(PepkioClient, "run", mock_run)

    res = runner.invoke(
        main,
        ["--api-key", "dummy", "run", "--sequence", "AAAAAAAAAAGAATTCAAAAAAAAAA"],
    )
    assert res.exit_code == 0
    assert "run_test_12345" in res.output
    assert "completed" in res.output
