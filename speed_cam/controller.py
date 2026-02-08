from __future__ import annotations

from collections import deque
from time import monotonic, sleep

from speed_cam.camera import Camera, CaptureRecord
from speed_cam.config import SpeedCamConfig
from speed_cam.sensors import RadarSensor


class SpeedCamController:
    def __init__(self, config: SpeedCamConfig, radar: RadarSensor, camera: Camera) -> None:
        self._config = config
        self._radar = radar
        self._camera = camera
        self._recent_speeds: deque[tuple[float, float]] = deque()
        self._last_capture_ts = float("-inf")

    def poll_once(self) -> CaptureRecord | None:
        reading = self._radar.read_speed()
        now = reading.timestamp_s

        if reading.speed_kph < self._config.min_trigger_kph:
            return None

        self._recent_speeds.append((now, reading.speed_kph))
        cutoff = now - self._config.sample_window_s
        while self._recent_speeds and self._recent_speeds[0][0] < cutoff:
            self._recent_speeds.popleft()

        if not self._recent_speeds:
            return None

        avg_speed = sum(speed for _, speed in self._recent_speeds) / len(self._recent_speeds)
        cooling_down = now - self._last_capture_ts < self._config.cooldown_s

        if avg_speed >= self._config.speed_limit_kph and not cooling_down:
            self._last_capture_ts = now
            return self._camera.capture(avg_speed, self._config.speed_limit_kph)
        return None

    def run(self, poll_interval_s: float = 0.1) -> None:
        while True:
            record = self.poll_once()
            if record:
                print(f"Captured speeding event: {record.image_path}")
            sleep(poll_interval_s)


def run_demo() -> None:
    from speed_cam.camera import FileCamera
    from speed_cam.sensors import SimulatedRadarSensor

    config = SpeedCamConfig()
    camera = FileCamera(output_dir=config.output_dir, save_metadata=config.save_metadata)
    radar = SimulatedRadarSensor()

    controller = SpeedCamController(config=config, radar=radar, camera=camera)
    print("Starting demo speed camera controller (Ctrl+C to stop)...")
    start = monotonic()
    try:
        while monotonic() - start < 5.0:
            controller.poll_once()
            sleep(0.1)
    except KeyboardInterrupt:
        pass
