from __future__ import annotations

from dataclasses import dataclass
from random import gauss
from time import monotonic
from typing import Protocol


@dataclass(frozen=True)
class RadarReading:
    timestamp_s: float
    speed_kph: float


class RadarSensor(Protocol):
    def read_speed(self) -> RadarReading:
        """Return latest speed reading in kph."""


class SimulatedRadarSensor:
    """Small development-time radar simulator.

    Produces noisy low speeds with occasional speeding events.
    """

    def __init__(self, base_speed_kph: float = 10.0, event_speed_kph: float = 68.0) -> None:
        self._base_speed_kph = base_speed_kph
        self._event_speed_kph = event_speed_kph
        self._counter = 0

    def read_speed(self) -> RadarReading:
        self._counter += 1
        event = self._counter % 15 in {0, 1, 2}
        target_speed = self._event_speed_kph if event else self._base_speed_kph
        noisy_speed = max(0.0, gauss(mu=target_speed, sigma=2.1))
        return RadarReading(timestamp_s=monotonic(), speed_kph=noisy_speed)
