import cv2
import numpy as np
from datetime import datetime

# Load image
img = cv2.imread("robot_view.png")
if img is None:
    print("robot_view.png not found")
    raise SystemExit(1)

out = img.copy()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create color masks
red_mask = cv2.inRange(hsv, (0,70,70), (15,255,255)) | \
           cv2.inRange(hsv, (160,70,70), (180,255,255))

green_mask = cv2.inRange(hsv, (35,50,50), (90,255,255))

# Clean noise
kernel = np.ones((5, 5), np.uint8)
red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

# Detection function
def detect(mask, label, color):
    count = 0
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 500:
            continue

        x, y, w, h = cv2.boundingRect(c)
        count += 1

        cv2.rectangle(out, (x, y), (x+w, y+h), color, 2)
        cv2.putText(out, f"{label} {count}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    return count

# Detect objects
disc_count = detect(red_mask, "Disc", (0,0,255))
box_count = detect(green_mask, "Box", (0,255,0))

# Add name + date
text = f"Galib Bin Mahamud {datetime.now().strftime('%Y-%m-%d')}"
cv2.putText(out, text, (20,50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

# Save & show
cv2.imwrite("annotated.png", out)
cv2.imshow("Detected Objects", out)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Disc:", disc_count)
print("Box:", box_count)