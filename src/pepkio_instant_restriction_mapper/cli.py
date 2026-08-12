"""Command-line interface for pepkio-instant-restriction-mapper."""

from __future__ import annotations

import json
import sys
from typing import Any

import click

from .client import PepkioClient
from .config import resolve_api_key, resolve_base_url
from .exceptions import PepkioAPIError


def _client(api_key: str | None, base_url: str | None) -> PepkioClient:
    resolved_base = resolve_base_url(base_url)
    return PepkioClient(
        api_key=api_key or resolve_api_key(base_url=resolved_base),
        base_url=resolved_base,
    )


@click.group()
@click.option(
    "--api-key",
    default=None,
    help="Pepkio API key (tools:run scope); else LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY from env",
)
@click.option(
    "--base-url",
    default=None,
    help="Tools API base URL (default: https://tools.pepkio.com or PEPKIO_API_BASE_URL)",
)
@click.pass_context
def main(ctx: click.Context, api_key: str | None, base_url: str | None) -> None:
    """Python client for Pepkio instant-restriction-mapper."""
    ctx.ensure_object(dict)
    ctx.obj["api_key"] = api_key
    ctx.obj["base_url"] = base_url


@main.command("manifest")
@click.option("--examples", is_flag=True, help="List example names only")
@click.pass_context
def manifest_cmd(ctx: click.Context, examples: bool) -> None:
    """Fetch and print the tool manifest."""
    try:
        with _client(ctx.obj["api_key"], ctx.obj["base_url"]) as client:
            data = client.get_manifest()
        if examples:
            for ex in data.get("examples", []):
                if isinstance(ex, dict) and ex.get("name"):
                    click.echo(ex["name"])
            return
        click.echo(json.dumps(data, indent=2))
    except (PepkioAPIError, ValueError) as e:
        click.echo(str(e), err=True)
        sys.exit(1)


@main.command("run")
@click.option("--example", "example_name", help="Run a named manifest example")
@click.option("--input-json", "input_json", help="Tool input as JSON object string")
@click.option("--sequence", help="DNA sequence string directly")
@click.option("--topology", default="circular", help="circular (default) or linear")
@click.option("--cut-frequency", default="1", help="1, 2, or all cuts (default: 1)")
@click.option("--label", help="Optional run label")
@click.option("--idempotency-key", help="Optional idempotency key")
@click.pass_context
def run_cmd(
    ctx: click.Context,
    example_name: str | None,
    input_json: str | None,
    sequence: str | None,
    topology: str,
    cut_frequency: str,
    label: str | None,
    idempotency_key: str | None,
) -> None:
    """Run the restriction mapper tool and output JSON result."""
    modes = [bool(example_name), bool(input_json), bool(sequence)]
    if sum(modes) != 1:
        raise click.UsageError("Provide exactly one of --example, --input-json, or --sequence")

    try:
        with _client(ctx.obj["api_key"], ctx.obj["base_url"]) as client:
            if example_name:
                inp: dict[str, Any] = client.get_example_input(example_name)
            elif input_json:
                inp = json.loads(input_json)
                if not isinstance(inp, dict):
                    raise click.ClickException("--input-json must be a JSON object")
            else:
                # Parse cut_frequency if integer string
                freq: int | str = int(cut_frequency) if cut_frequency.isdigit() else cut_frequency
                inp = {
                    "sequence": sequence,
                    "topology": topology,
                    "cut_frequency": freq,
                }

            result = client.run(
                inp,
                idempotency_key=idempotency_key,
                label=label,
            )
        click.echo(json.dumps(result.model_dump(exclude_none=True), indent=2))
    except (PepkioAPIError, ValueError, json.JSONDecodeError) as e:
        click.echo(str(e), err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
