import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt", target_class="person"):
        self.model = YOLO(model_path)
        self.target_class = target_class

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        best = None
        best_conf = 0

        annotated = frame.copy()

        for box in results[0].boxes:
            class_name = self.model.names[int(box.cls)]
            confidence = float(box.conf)

            if class_name != self.target_class:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated, f"person {confidence:.2f}",
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.circle(annotated, (cx, cy), 6, (0, 0, 255), -1)

            if confidence > best_conf:
                best_conf = confidence
                best = (cx, cy)

        if best:
            return best[0], best[1], annotated

        return None, None, annotated