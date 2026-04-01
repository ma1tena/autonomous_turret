# autonomous_turret

# Camera auto-tracking project

This is my project for the *Deep Learning for Computer Vision* course.

The idea is simple: the camera detects a person and follows them automatically using two servo motors (pan/tilt).

---

## How it works

- Camera captures video
- YOLO model detects a person
- I take the center of the bounding box
- If the person is not in the center → camera moves
- ESP32 controls the servos

---

## Tech stack

- Python
- OpenCV
- YOLO (Ultralytics)
- ESP32
- Serial communication

---

## Project structure
