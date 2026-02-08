from pathlib import Path

from speed_cam.camera import FileCamera
from speed_cam.config import SpeedCamConfig
from speed_cam.controller import SpeedCamController
from speed_cam.sensors import RadarReading


class StubRadar:
    def __init__(self, speeds: list[float]) -> None:
        self._speeds = iter(speeds)
        self._ts = 0.0

    def read_speed(self) -> RadarReading:
        self._ts += 0.1
        return RadarReading(timestamp_s=self._ts, speed_kph=next(self._speeds))


def test_capture_happens_when_average_above_limit(tmp_path: Path) -> None:
    config = SpeedCamConfig(speed_limit_kph=50, cooldown_s=10, output_dir=tmp_path)
    radar = StubRadar([40, 60, 65, 67])
    camera = FileCamera(output_dir=tmp_path)
    controller = SpeedCamController(config=config, radar=radar, camera=camera)

    assert controller.poll_once() is None
    record = controller.poll_once()

    assert record is not None
    assert record.image_path.exists()
    assert record.metadata_path is not None and record.metadata_path.exists()


def test_cooldown_prevents_duplicate_captures(tmp_path: Path) -> None:
    config = SpeedCamConfig(speed_limit_kph=40, cooldown_s=5, output_dir=tmp_path)
    radar = StubRadar([45, 47, 49, 51])
    camera = FileCamera(output_dir=tmp_path)
    controller = SpeedCamController(config=config, radar=radar, camera=camera)

    first = controller.poll_once()
    second = controller.poll_once()

    assert first is not None
    assert second is None
