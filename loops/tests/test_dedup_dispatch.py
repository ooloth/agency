"""Tests for the scan loop's dedup dispatch logic."""

from unittest.mock import MagicMock, patch

from loops.scan import _dispatch_dedup_actions


def test_post_action_creates_issue() -> None:
    """A 'post' action calls create_issue with the title, body, and merged labels."""
    actions = [{"action": "post", "title": "New bug", "body": "details", "label": "sev:high"}]
    create = MagicMock()

    with patch("loops.scan.create_issue", create):
        _dispatch_dedup_actions(actions, extra_labels=["autonomous"], dry_run=False)

    create.assert_called_once_with("New bug", "details", ["sev:high", "autonomous"])


def test_post_action_defaults_to_sev_medium() -> None:
    """A 'post' action without a label defaults to sev:medium."""
    actions = [{"action": "post", "title": "Bug", "body": "details"}]
    create = MagicMock()

    with patch("loops.scan.create_issue", create):
        _dispatch_dedup_actions(actions, extra_labels=[], dry_run=False)

    create.assert_called_once_with("Bug", "details", ["sev:medium"])


def test_comment_action_posts_on_existing_issue() -> None:
    """A 'comment' action calls comment_on_issue with the target and body."""
    actions = [
        {
            "action": "comment",
            "target_issue": 42,
            "comment_body": "**New observations from scan:**\n\nnew evidence",
            "reason": "same root cause as #42",
        }
    ]
    comment = MagicMock()

    with patch("loops.scan.comment_on_issue", comment):
        _dispatch_dedup_actions(actions, extra_labels=[], dry_run=False)

    comment.assert_called_once_with(42, "**New observations from scan:**\n\nnew evidence")


def test_skip_action_does_not_call_github() -> None:
    """A 'skip' action logs but does not call create_issue or comment_on_issue."""
    actions = [{"action": "skip", "title": "Dup bug", "reason": "identical to #7"}]
    create = MagicMock()
    comment = MagicMock()

    with (
        patch("loops.scan.create_issue", create),
        patch("loops.scan.comment_on_issue", comment),
    ):
        _dispatch_dedup_actions(actions, extra_labels=[], dry_run=False)

    create.assert_not_called()
    comment.assert_not_called()


def test_unknown_action_does_not_call_github() -> None:
    """An unrecognised action logs a warning but does not call GitHub."""
    actions = [{"action": "merge", "title": "?"}]
    create = MagicMock()
    comment = MagicMock()

    with (
        patch("loops.scan.create_issue", create),
        patch("loops.scan.comment_on_issue", comment),
    ):
        _dispatch_dedup_actions(actions, extra_labels=[], dry_run=False)

    create.assert_not_called()
    comment.assert_not_called()


def test_dry_run_does_not_call_github() -> None:
    """In dry-run mode, no GitHub calls are made for any action type."""
    actions = [
        {"action": "post", "title": "New", "body": "b", "label": "sev:low"},
        {"action": "comment", "target_issue": 1, "comment_body": "c", "reason": "r"},
        {"action": "skip", "title": "Old", "reason": "dup"},
    ]
    create = MagicMock()
    comment = MagicMock()

    with (
        patch("loops.scan.create_issue", create),
        patch("loops.scan.comment_on_issue", comment),
    ):
        _dispatch_dedup_actions(actions, extra_labels=["autonomous"], dry_run=True)

    create.assert_not_called()
    comment.assert_not_called()


def test_mixed_actions_dispatch_correctly() -> None:
    """A batch with all three action types dispatches each one correctly."""
    actions = [
        {"action": "post", "title": "New bug", "body": "details", "label": "sev:high"},
        {
            "action": "comment",
            "target_issue": 5,
            "comment_body": "extra context",
            "reason": "overlap",
        },
        {"action": "skip", "title": "Dup", "reason": "same as #5"},
    ]
    create = MagicMock()
    comment = MagicMock()

    with (
        patch("loops.scan.create_issue", create),
        patch("loops.scan.comment_on_issue", comment),
    ):
        _dispatch_dedup_actions(actions, extra_labels=["autonomous"], dry_run=False)

    create.assert_called_once_with("New bug", "details", ["sev:high", "autonomous"])
    comment.assert_called_once_with(5, "extra context")
