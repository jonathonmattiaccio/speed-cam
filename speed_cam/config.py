from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SpeedCamConfig:
    """Runtime configuration for speed camera behavior."""

    speed_limit_kph: float = 50.0
    min_trigger_kph: float = 5.0
    sample_window_s: float = 0.4
    cooldown_s: float = 3.0
    output_dir: Path = Path("captures")
    save_metadata: bool = True
