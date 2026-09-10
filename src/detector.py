from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from ultralytics import YOLO

from src.config import (
    CONFIDENCE_THRESHOLD,
    IMAGE_SIZE,
    IOU_THRESHOLD,
    MODEL_PATH,
    RULES_PATH,
)
from src.safety_engine import SafetyRuleEngine


class SafeVisionDetector:
    """
    Production inference wrapper for SafeVision AI.

    Handles:
    - YOLO model loading
    - Image inference
    - Detection extraction
    - Safety rule analysis
    - Annotated image generation
    """

    def __init__(
        self,
        model_path: str | Path = MODEL_PATH,
        rules_path: str | Path = RULES_PATH,
    ):
        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        self.model = YOLO(str(self.model_path))

        self.safety_engine = SafetyRuleEngine(rules_path)

    def predict(
        self,
        image: Image.Image | np.ndarray,
        conf: float = CONFIDENCE_THRESHOLD,
        iou: float = IOU_THRESHOLD,
        imgsz: int = IMAGE_SIZE,
    ) -> dict[str, Any]:
        """
        Run YOLO inference and return structured results.
        """

        # --------------------------------------------------------
        # Normalize image input
        # --------------------------------------------------------

        if isinstance(image, Image.Image):
            image_rgb = image.convert("RGB")
            image_array = np.array(image_rgb)

        elif isinstance(image, np.ndarray):
            image_array = image

            if image_array.ndim == 2:
                image_array = np.stack(
                    [image_array] * 3,
                    axis=-1,
                )

            if image_array.shape[-1] == 4:
                image_array = image_array[:, :, :3]

        else:
            raise TypeError(
                "Image must be a PIL.Image.Image or numpy.ndarray."
            )

        # --------------------------------------------------------
        # YOLO inference
        # --------------------------------------------------------

        results = self.model.predict(
            source=image_array,
            conf=conf,
            iou=iou,
            imgsz=imgsz,
            verbose=False,
        )

        result = results[0]

        # --------------------------------------------------------
        # Extract detections
        # --------------------------------------------------------

        detections: list[dict[str, Any]] = []

        if result.boxes is not None:

            boxes = result.boxes

            for index in range(len(boxes)):

                class_id = int(boxes.cls[index].item())
                confidence = float(boxes.conf[index].item())

                class_name = self.model.names[class_id]

                xyxy = boxes.xyxy[index].cpu().numpy().tolist()

                detections.append(
                    {
                        "class_id": class_id,
                        "class_name": class_name,
                        "confidence": confidence,
                        "bbox": xyxy,
                    }
                )

        # --------------------------------------------------------
        # Safety analysis
        # --------------------------------------------------------

        safety_analysis = self.safety_engine.analyze(
            detections
        )

        # --------------------------------------------------------
        # Annotated image
        # --------------------------------------------------------

        annotated_bgr = result.plot()

        annotated_rgb = annotated_bgr[:, :, ::-1]

        annotated_image = Image.fromarray(annotated_rgb)

        # --------------------------------------------------------
        # Final structured result
        # --------------------------------------------------------

        return {
            "detections": detections,
            "detection_count": len(detections),
            "safety": safety_analysis,
            "annotated_image": annotated_image,
        }