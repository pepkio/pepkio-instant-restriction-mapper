# SPDX-License-Identifier: MIT
"""Typed API request/response models for Pepkio instant-restriction-mapper."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .exceptions import PepkioAPIError


class RestrictionMapperInput(BaseModel):
    """Input model for instant-restriction-mapper tool."""

    model_config = ConfigDict(extra="allow")

    sequence: str = Field(..., description="DNA sequence (plain or FASTA)")
    sequence_name: str | None = Field(
        default=None, description="Optional sequence label for exports"
    )
    topology: str | None = Field(default="circular", description="circular (default) or linear")
    cut_frequency: int | str | None = Field(default=1, description="1, 2, or all cuts (default 1)")
    hide_short_sites: bool | None = Field(
        default=True,
        description="Hide enzymes with recognition sites shorter than 6 bp (default true)",
    )
    show_isoschizomers: bool | None = Field(
        default=False, description="Show redundant isoschizomers (default false)"
    )
    selected_enzymes: list[str] | None = Field(
        default=None, description="Enzyme names for fragment / gel preview"
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert input to payload dictionary, dropping None values."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class RunOptions(BaseModel):
    """Optional configuration for POST /run."""

    idempotency_key: str | None = None
    label: str | None = None


class RunResult(BaseModel):
    """Tool run response envelope."""

    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | str | None = None
    result_url: str | None = None
    permalink: str | None = None
    duration_ms: int | None = None

    def raise_for_error(self) -> None:
        """Raise PepkioAPIError if error field is set or if result contains an error."""
        if self.error is not None:
            if isinstance(self.error, dict):
                msg = self.error.get("message", "Tool run failed")
                code = self.error.get("code")
                details = (
                    self.error.get("details") if isinstance(self.error.get("details"), dict) else {}
                )
            else:
                msg = str(self.error)
                code = "RUN_ERROR"
                details = {}
            raise PepkioAPIError(
                msg,
                code=code,
                details=details,
                response_body={"run_id": self.run_id, "status": self.status, "error": self.error},
            )

        if isinstance(self.result, dict) and self.result.get("error"):
            err_val = self.result["error"]
            msg = err_val.get("message") if isinstance(err_val, dict) else str(err_val)
            raise PepkioAPIError(
                msg,
                code="TOOL_RESULT_ERROR",
                response_body={"run_id": self.run_id, "status": self.status, "result": self.result},
            )


def parse_run_response(data: dict[str, Any]) -> RunResult:
    """Parse a run API JSON response into RunResult."""
    return RunResult.model_validate(data)
