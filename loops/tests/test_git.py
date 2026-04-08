"""Tests for git helpers."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from loops.common.errors import CommitRejectedError
from loops.common.git import commit_if_dirty


def _mock_git_for_dirty_tree(commit_returncode: int, commit_stderr: str = "") -> MagicMock:
    """Return a mock that reports a dirty tree, stages OK, then commits with the given result."""

    def side_effect(*args: str, **kwargs: object) -> MagicMock:
        cmd = args[0] if args else ""
        match cmd:
            case "status":
                return MagicMock(stdout="M file.py\n")
            case "add":
                return MagicMock()
            case "commit":
                result = MagicMock(returncode=commit_returncode, stderr=commit_stderr)
                if kwargs.get("check", True) and commit_returncode != 0:
                    msg = "should not be reached with check=False"
                    raise RuntimeError(msg)
                return result
            case _:
                return MagicMock()

    return MagicMock(side_effect=side_effect)


class TestCommitIfDirty:
    def test_successful_commit(self) -> None:
        mock_git = _mock_git_for_dirty_tree(commit_returncode=0)
        with patch("loops.common.git.git", mock_git):
            assert commit_if_dirty("test msg", Path("/repo")) is True

    def test_clean_tree_returns_false(self) -> None:
        mock_git = MagicMock(return_value=MagicMock(stdout=""))
        with patch("loops.common.git.git", mock_git):
            assert commit_if_dirty("test msg", Path("/repo")) is False

    def test_commit_rejection_raises_commit_rejected_error(self) -> None:
        mock_git = _mock_git_for_dirty_tree(commit_returncode=1, commit_stderr="ruff-check failed")
        with (
            patch("loops.common.git.git", mock_git),
            pytest.raises(CommitRejectedError, match="ruff-check failed"),
        ):
            commit_if_dirty("test msg", Path("/repo"))
