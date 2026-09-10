import json
from pathlib import Path
from typing import Any


class SafetyRuleEngine:
    """
    Detection-level PPE safety analysis engine.

    Important:
    - Explicit negative classes are confirmed violations.
    - Missing positive detections are NOT automatically violations.
    - Requirements without explicit negative classes are treated as
      unmeasurable when the PPE item is not observed.
    """

    def __init__(self, rules_path: str | Path):
        self.rules_path = Path(rules_path)

        with open(self.rules_path, "r", encoding="utf-8") as file:
            self.rules = json.load(file)

    def analyze(self, detections: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Analyze YOLO detections and calculate PPE compliance
        and a weighted measurable safety score.
        """

        class_counts: dict[str, int] = {}

        for detection in detections:
            class_name = detection["class_name"]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        compliance = {}
        violations = []

        measurable_weights = 0
        weighted_score = 0

        for requirement, rule in self.rules.items():

            positive_class = rule["positive_class"]
            violation_class = rule.get("violation_class")
            weight = rule["weight"]

            positive_count = class_counts.get(positive_class, 0)

            violation_count = (
                class_counts.get(violation_class, 0)
                if violation_class
                else 0
            )

            # ----------------------------------------------------
            # Explicit violation detected
            # ----------------------------------------------------
            if violation_count > 0:

                total_observed = positive_count + violation_count

                compliance_percentage = (
                    positive_count / total_observed * 100
                    if total_observed > 0
                    else None
                )

                compliance[requirement] = compliance_percentage

                violations.append(
                    {
                        "requirement": requirement,
                        "category": rule["category"],
                        "violation_class": violation_class,
                        "count": violation_count,
                    }
                )

                measurable_weights += weight

                if compliance_percentage is not None:
                    weighted_score += (
                        compliance_percentage * weight / 100
                    )

            # ----------------------------------------------------
            # Positive PPE detected
            # ----------------------------------------------------
            elif positive_count > 0:

                compliance[requirement] = 100.0

                measurable_weights += weight
                weighted_score += weight

            # ----------------------------------------------------
            # No evidence
            # ----------------------------------------------------
            else:

                compliance[requirement] = None

        # --------------------------------------------------------
        # Final safety score
        # --------------------------------------------------------

        if measurable_weights > 0:

            safety_score = (
                weighted_score / measurable_weights * 100
            )

            score_status = "measurable"

        else:

            safety_score = None
            score_status = "insufficient_evidence"

        return {
            "safety_score": safety_score,
            "score_status": score_status,
            "compliance": compliance,
            "violations": violations,
            "class_counts": class_counts,
        }