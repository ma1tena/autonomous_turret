# Autonomous Turret – Camera Auto-Tracking System

## Overview

This project was developed as part of the Deep Learning for Computer Vision course.

The goal is to build a real-time system that detects a person and keeps them centered in the camera frame using a pan-tilt mechanism driven by servo motors.

The system combines computer vision (YOLO), control logic (PID), and embedded hardware (ESP32).

## System Architecture

Camera → YOLO Detection → Target Center → PID Controller → ESP32 → Servos → Camera Movement

## How It Works

The webcam captures a live video stream. A YOLO model processes each frame and detects objects. The system filters detections and keeps only the "person" class. The center of the bounding box is calculated and compared to the center of the frame. The difference between these points is treated as an error.

A PID controller uses this error to compute correction values. These values are sent to the ESP32 via serial communication. The ESP32 adjusts the servo motors so that the camera follows the person.

## Features

Real-time human detection using YOLOv8  
Smooth tracking using a PID controller  
Dead zone to reduce jitter near the center  
Serial communication with ESP32  
Modular code structure  

## Tech Stack

Python  
OpenCV  
Ultralytics YOLO (YOLOv8)  
ESP32  
Serial communication  
PID control  

## Project Structure

.
├── main.py          # main tracking loop
├── detector.py      # object detection using YOLO
├── pid.py           # PID controller
├── serial_comm.py   # communication with ESP32

## Core Components

Object detection (detector.py) uses YOLOv8 (yolov8n.pt), filters only the "person" class, selects the detection with the highest confidence, and returns the center of the bounding box.

PID controller (pid.py) implements proportional control with optional integral and derivative terms. Currently only the proportional term is used for stable behavior.

Tracking logic (main.py) calculates the error between the target and frame center, applies PID correction, uses a dead zone to prevent jitter, and sends commands to ESP32.

Serial communication (serial_comm.py) sends servo angles in the format "pan,tilt", for example:
90,45

## Configuration

PAN_KP  = 0.02  
TILT_KP = 0.02  
DEAD_ZONE = 30  
SERIAL_PORT = "/dev/cu.usbserial-0001"

## How to Run

Install dependencies:
pip install opencv-python ultralytics pyserial

Run the program:
python main.py

Press Q to exit.

## Testing Without Hardware

You can test communication using a serial monitor. Send:
90,45

Expected response:
Received → pan=90° tilt=45°

## Limitations

The system works best with a single visible person. It is sensitive to lighting conditions. It does not support multi-object tracking. PID parameters are tuned manually. A wired connection is required.

## Future Work

Possible improvements include adding multi-person tracking, using filters for smoother motion, automatic PID tuning, wireless communication, and improving the mechanical design of the gimbal.

## Repository

https://github.com/ma1tena/autonomous_turret
