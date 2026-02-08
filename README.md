# Raspberry Pi Speed Camera (Starter Code)

This repository now contains a small Python starter architecture for a speed camera project using:

- Doppler radar for speed sampling
- Camera trigger when average speed is above a threshold
- Optional metadata output for auditing/testing

## Design goals

- Keep hardware-specific code behind interfaces (`RadarSensor`, `Camera`)
- Make core enforcement logic testable without real hardware
- Provide a simulated radar + file camera for local development

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest
pytest -q
```

Run a short demo loop (5 seconds) that generates placeholder captures:

```bash
python -c "from speed_cam import run_demo; run_demo()"
```

Outputs will be written to `captures/` by default.

## Where to connect real hardware

- Replace `SimulatedRadarSensor` with a radar implementation that reads serial/UART/SPI GPIO data and returns `RadarReading`.
- Replace `FileCamera` with a `picamera2` implementation that captures real images.
- If you add a flash, trigger it in your camera implementation right before exposure.

## Next recommended improvements

1. Add plate recognition pipeline (if legal/needed in your region).
2. Add SQLite logging and upload queue.
3. Add calibration mode for radar filtering and false-positive suppression.
4. Add day/night profile switching (different shutter/flash behavior).
