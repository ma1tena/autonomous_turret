import cv2
from detector import ObjectDetector
from serial_comm import SerialComm
from pid import PIDController
import time

# --- Config ---
CAMERA_INDEX = 0
TARGET_CLASS = "person"
ENABLE_SERIAL = True
SERIAL_PORT = "/dev/cu.usbserial-0001"  # change to your port

# --- PID Tuning values ---
# Start with only Kp, keep Ki and Kd at 0 first
# Increase Kp slowly until it tracks without overshooting
PAN_KP  = 0.02
PAN_KI  = 0.0
PAN_KD  = 0.0

TILT_KP = 0.02
TILT_KI = 0.0
TILT_KD = 0.0

# Dead zone — ignore small errors (pixels)
# Prevents servos jittering when person is near center
DEAD_ZONE = 30

def draw_crosshair(frame):
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    color = (255, 255, 255)
    cv2.line(frame, (cx, 0), (cx, h), color, 1)
    cv2.line(frame, (0, cy), (w, cy), color, 1)
    cv2.circle(frame, (cx, cy), 10, color, 1)
    cv2.circle(frame, (cx, cy), DEAD_ZONE, (100, 100, 100), 1)  # dead zone ring
    return frame, cx, cy

def main():
    detector = ObjectDetector(target_class=TARGET_CLASS)
    cap = cv2.VideoCapture(CAMERA_INDEX)

    pid_pan  = PIDController(kp=PAN_KP,  ki=PAN_KI,  kd=PAN_KD)
    pid_tilt = PIDController(kp=TILT_KP, ki=TILT_KI, kd=TILT_KD)

    pan_angle  = 90  # start centered
    tilt_angle = 90

    comm = None
    if ENABLE_SERIAL:
        try:
            comm = SerialComm(port=SERIAL_PORT)
        except Exception as e:
            print(f"Serial connection failed: {e}")
            print("Running without ESP32...")

    print("Starting tracker... press Q to quit\n")

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not found")
            break

        # Calculate real time delta between frames
        now = time.time()
        dt = now - prev_time
        prev_time = now

        frame_h, frame_w = frame.shape[:2]
        frame_cx, frame_cy = frame_w // 2, frame_h // 2

        obj_cx, obj_cy, annotated = detector.detect(frame)
        annotated, _, _ = draw_crosshair(annotated)

        if obj_cx is not None:
            error_x = obj_cx - frame_cx
            error_y = obj_cy - frame_cy

            # Dead zone — don't move if error is small
            if abs(error_x) > DEAD_ZONE:
                pan_angle  -= pid_pan.compute(error_x, dt)  # flipped
            else:
                pid_pan.reset()

            if abs(error_y) > DEAD_ZONE:
                tilt_angle += pid_tilt.compute(error_y, dt)
            else:
                pid_tilt.reset()

            # Clamp to safe servo range
            pan_angle  = max(0, min(180, pan_angle))
            tilt_angle = max(0, min(180, tilt_angle))

            pan_int  = int(pan_angle)
            tilt_int = int(tilt_angle)

            print(f"Error: ({error_x:+d}, {error_y:+d}) | "
                  f"→ pan={pan_int}° tilt={tilt_int}°")

            if comm:
                comm.send_angles(pan_int, tilt_int)

            cv2.line(annotated, (frame_cx, frame_cy), (obj_cx, obj_cy), (0, 255, 255), 1)
            cv2.putText(annotated, f"pan={pan_int} tilt={tilt_int}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated, f"error=({error_x:+d}, {error_y:+d})",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        else:
            # Reset PID when target is lost so it doesn't accumulate
            pid_pan.reset()
            pid_tilt.reset()
            print("No target detected")

        cv2.imshow("Pan-Tilt Tracker", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if comm:
        comm.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()