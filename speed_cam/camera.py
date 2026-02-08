from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class CaptureRecord:
    image_path: Path
    metadata_path: Path | None


class Camera(Protocol):
    def capture(self, speed_kph: float, speed_limit_kph: float) -> CaptureRecord:
        """Capture an image and optionally metadata."""


class FileCamera:
    """Filesystem-backed stand-in for a real Pi camera implementation."""

    def __init__(self, output_dir: Path, save_metadata: bool = True) -> None:
        self._output_dir = output_dir
        self._save_metadata = save_metadata
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def capture(self, speed_kph: float, speed_limit_kph: float) -> CaptureRecord:
        ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        image_path = self._output_dir / f"speeding-{ts}.jpg"
        image_path.write_bytes(b"JPEG_PLACEHOLDER")

        metadata_path = None
        if self._save_metadata:
            metadata_path = self._output_dir / f"speeding-{ts}.json"
            metadata_path.write_text(
                json.dumps(
                    {
                        "captured_at_utc": ts,
                        "speed_kph": round(speed_kph, 2),
                        "speed_limit_kph": speed_limit_kph,
                        "over_limit_kph": round(speed_kph - speed_limit_kph, 2),
                    },
                    indent=2,
                )
            )

        return CaptureRecord(image_path=image_path, metadata_path=metadata_path)
