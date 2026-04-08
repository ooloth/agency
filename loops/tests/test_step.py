"""Tests for step() error persistence behaviour."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from loops.common.errors import AgentError
from loops.common.step import step


class _FakeCtx:
    """Minimal StepCtx implementation for testing."""

    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir
        self.steps: list[dict] = []
        self.refs: list[dict] = []


def test_agent_error_persisted_and_reraised(tmp_path: Path) -> None:
    """When agent() raises AgentError, step() persists error details and re-raises."""
    ctx = _FakeCtx(tmp_path)

    with (
        patch(
            "loops.common.step.agent",
            side_effect=AgentError("crashed", step="find", exit_code=1, output="raw"),
        ),
        pytest.raises(AgentError, match="crashed"),
    ):
        step(ctx, "find", "prompts/scan/find.md", "context")

    # Error detail persisted to run directory
    error_file = tmp_path / "find-error.json"
    assert error_file.exists()
    detail = json.loads(error_file.read_text())
    assert detail["error_type"] == "AgentError"
    assert detail["step"] == "find"
    assert detail["exit_code"] == 1
    assert detail["output"] == "raw"

    # Step recorded with error in ctx.steps
    assert len(ctx.steps) == 1
    assert ctx.steps[0]["name"] == "find"
    assert "error" in ctx.steps[0]
    assert ctx.steps[0]["duration_seconds"] >= 0


def test_success_path_unchanged(tmp_path: Path) -> None:
    """On success, step() records timing and reflections as before."""
    ctx = _FakeCtx(tmp_path)
    agent_output = {"findings": [], "reflections": ["note"]}

    with patch("loops.common.step.agent", return_value=agent_output):
        result = step(ctx, "find", "prompts/scan/find.md", "context")

    assert result == agent_output
    assert len(ctx.steps) == 1
    assert "error" not in ctx.steps[0]
    assert ctx.refs == [{"step": "find", "text": "note"}]

    # Output persisted, no error file
    assert (tmp_path / "find.json").exists()
    assert not (tmp_path / "find-error.json").exists()
