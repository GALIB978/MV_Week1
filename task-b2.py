import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

img_path = os.path.join(HERE, "robot_view.png")
img = cv2.imread(img_path)
if img is None:
    print("robot_view.png not found")
    raise SystemExit(1)

out = img.copy()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# RED mask (two HSV ranges)
lower_red1 = np.array([0, 80, 80])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 80, 80])
upper_red2 = np.array([180, 255, 255])
mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

# GREEN mask
lower_green = np.array([35, 60, 60])
upper_green = np.array([90, 255, 255])
mask_green = cv2.inRange(hsv, lower_green, upper_green)

# Clean noise
kernel = np.ones((5, 5), np.uint8)
mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

def detect(mask, label):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area < 500:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(out, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        count += 1
    return count

disc = detect(mask_red, "Disc")
box = detect(mask_green, "Box")

out_path = os.path.join(HERE, "annotated.png")
cv2.imwrite(out_path, out)
cv2.imshow("Detected Objects", out)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Disc:", disc)
print("Box:", box)
print("annotated.png saved")