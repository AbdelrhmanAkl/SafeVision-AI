from typing import Any


def format_percentage(value: float | None) -> str:
    """Format a percentage value for display."""

    if value is None:
        return "N/A"

    return f"{value:.1f}%"


def get_safety_status(
    safety_score: float | None,
    score_status: str,
) -> str:
    """Return a human-readable safety status."""

    if score_status == "insufficient_evidence":
        return "Insufficient Evidence"

    if safety_score is None:
        return "Insufficient Evidence"

    if safety_score >= 80:
        return "Safe"

    if safety_score >= 50:
        return "Needs Attention"

    return "High Risk"


def get_detection_summary(
    detections: list[dict[str, Any]],
) -> dict[str, int]:
    """Count detected object classes."""

    summary: dict[str, int] = {}

    for detection in detections:
        class_name = detection["class_name"]
        summary[class_name] = summary.get(class_name, 0) + 1

    return summary