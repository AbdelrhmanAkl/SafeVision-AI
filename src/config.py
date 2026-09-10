from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "best.pt"

RULES_PATH = PROJECT_ROOT / "config" / "safety_rules_config.json"

EVALUATION_PATH = (
    PROJECT_ROOT / "evaluation" / "batch_safety_results.json"
)


# ============================================================
# YOLO INFERENCE CONFIGURATION
# ============================================================

CONFIDENCE_THRESHOLD = 0.25

IOU_THRESHOLD = 0.45

IMAGE_SIZE = 640


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

APP_TITLE = "SafeVision AI"

APP_SUBTITLE = "Real-Time PPE & Workplace Safety Detection"


# ============================================================
# SUPPORTED IMAGE TYPES
# ============================================================

SUPPORTED_IMAGE_TYPES = [
    "jpg",
    "jpeg",
    "png",
    "webp",
]


# ============================================================
# VALIDATE REQUIRED FILES
# ============================================================

def validate_project_files() -> None:
    """
    Validate that all required production artifacts exist.
    """

    required_files = {
        "YOLO model": MODEL_PATH,
        "Safety rules": RULES_PATH,
        "Evaluation results": EVALUATION_PATH,
    }

    missing_files = [
        f"{name}: {path}"
        for name, path in required_files.items()
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing required project files:\n"
            + "\n".join(missing_files)
        )