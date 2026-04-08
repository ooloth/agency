"""Tests for gh() retry logic on transient CLI failures."""

import subprocess
from unittest.mock import patch

import pytest

from loops.common.errors import GithubError
from loops.common.github import MAX_RETRIES, gh


def _make_completed(stdout: str = "") -> subprocess.CompletedProcess:
    return subprocess.CompletedProcess(args=["gh"], returncode=0, stdout=stdout, stderr="")


def _make_error(returncode: int = 1) -> subprocess.CalledProcessError:
    return subprocess.CalledProcessError(returncode, cmd=["gh", "issue", "list"])


def test_transient_failure_retries_and_succeeds() -> None:
    """A transient failure on the first call retries and succeeds, logging the retry."""
    effects = [_make_error(), _make_completed(stdout="[]")]
    with (
        patch("loops.common.github._gh_path", return_value="/usr/bin/gh"),
        patch("subprocess.run", side_effect=effects) as mock_run,
        patch("time.sleep") as mock_sleep,
        patch("loops.common.github.log") as mock_log,
    ):
        result = gh("issue", "list", "--json", "number")

    assert result.stdout == "[]"
    assert mock_run.call_count == 2
    mock_sleep.assert_called_once_with(1)  # first backoff = 1s
    mock_log.warning.assert_called_once()
    assert "attempt 1" in mock_log.warning.call_args[0][0] % mock_log.warning.call_args[0][1:]


def test_no_retry_on_success() -> None:
    """Under normal conditions, completes in one call with no retries."""
    with (
        patch("loops.common.github._gh_path", return_value="/usr/bin/gh"),
        patch("subprocess.run", return_value=_make_completed(stdout="[]")) as mock_run,
        patch("time.sleep") as mock_sleep,
    ):
        result = gh("issue", "list", "--json", "number")

    assert result.stdout == "[]"
    assert mock_run.call_count == 1
    mock_sleep.assert_not_called()


def test_exhausted_retries_raises_with_command_and_count() -> None:
    """After exhausting retries, raises naming the failed command and attempt count."""
    effects = [_make_error() for _ in range(MAX_RETRIES + 1)]
    with (
        patch("loops.common.github._gh_path", return_value="/usr/bin/gh"),
        patch("subprocess.run", side_effect=effects),
        patch("time.sleep"),
        pytest.raises(GithubError, match=str(MAX_RETRIES + 1)) as exc_info,
    ):
        gh("issue", "list", "--json", "number")

    assert "issue list --json number" in exc_info.value.cmd
    assert exc_info.value.attempts == MAX_RETRIES + 1


def test_no_retry_when_check_false() -> None:
    """When check=False, no retry is attempted even on failure."""
    failing = _make_completed()
    failing.returncode = 1
    with (
        patch("loops.common.github._gh_path", return_value="/usr/bin/gh"),
        patch("subprocess.run", return_value=failing) as mock_run,
        patch("time.sleep") as mock_sleep,
    ):
        result = gh("issue", "list", check=False)

    assert result.returncode == 1
    assert mock_run.call_count == 1
    mock_sleep.assert_not_called()


def test_backoff_is_exponential() -> None:
    """Backoff delays double with each retry: 1s, 2s, 4s."""
    effects = [_make_error() for _ in range(MAX_RETRIES)] + [_make_completed()]
    with (
        patch("loops.common.github._gh_path", return_value="/usr/bin/gh"),
        patch("subprocess.run", side_effect=effects),
        patch("time.sleep") as mock_sleep,
    ):
        gh("issue", "list")

    delays = [call.args[0] for call in mock_sleep.call_args_list]
    assert delays == [1, 2, 4]
