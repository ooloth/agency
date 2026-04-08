"""Domain-specific error types with structured context.

All types subclass RuntimeError so existing bare try/finally cleanup is unchanged.
"""

from pathlib import Path


class AgentError(RuntimeError):
    """The Claude agent subprocess failed, produced no output, or returned unparseable output."""

    def __init__(
        self,
        message: str,
        *,
        step: str = "",
        exit_code: int | None = None,
        output: str = "",
    ) -> None:
        """Store the agent step name, optional exit code, and raw output."""
        super().__init__(message)
        self.step = step
        self.exit_code = exit_code
        self.output = output


class GitError(RuntimeError):
    """A git precondition check failed (dirty tree, branch already exists, etc.)."""

    def __init__(self, message: str, *, path: Path | None = None) -> None:
        """Store the repo path where the precondition failed."""
        super().__init__(message)
        self.path = path


class CommitRejectedError(GitError):
    """A git commit was rejected (e.g. by pre-commit hooks)."""

    def __init__(self, message: str, *, path: Path | None = None, stderr: str = "") -> None:
        """Store the repo path and stderr from the failed commit."""
        super().__init__(message, path=path)
        self.stderr = stderr


class GithubError(RuntimeError):
    """The gh CLI failed after exhausting retries."""

    def __init__(
        self,
        message: str,
        *,
        cmd: str = "",
        attempts: int = 0,
        last_stderr: str = "",
    ) -> None:
        """Store the failed command, attempt count, and last stderr."""
        super().__init__(message)
        self.cmd = cmd
        self.attempts = attempts
        self.last_stderr = last_stderr


class CommandError(RuntimeError):
    """An arbitrary shell command exited with a non-zero status."""

    def __init__(
        self,
        message: str,
        *,
        cmd: str = "",
        exit_code: int | None = None,
    ) -> None:
        """Store the command string and exit code."""
        super().__init__(message)
        self.cmd = cmd
        self.exit_code = exit_code
