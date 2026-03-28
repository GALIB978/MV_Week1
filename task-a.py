import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

img_path = os.path.join(HERE, "robot_view.png")
img = cv2.imread(img_path)
if img is None:
    print("robot_view.png not found")
    raise SystemExit(1)

b, g, r = cv2.split(img)

r_img = cv2.cvtColor(r, cv2.COLOR_GRAY2BGR)
g_img = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
b_img = cv2.cvtColor(b, cv2.COLOR_GRAY2BGR)

W, H = 420, 300
img = cv2.resize(img, (W, H))
r_img = cv2.resize(r_img, (W, H))
g_img = cv2.resize(g_img, (W, H))
b_img = cv2.resize(b_img, (W, H))

def add_title(im, title):
    bar_h = 40
    bar = np.full((bar_h, im.shape[1], 3), 245, dtype=np.uint8)
    cv2.putText(bar, title, (12, 27),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2, cv2.LINE_AA)
    out = np.vstack((bar, im))
    out = cv2.copyMakeBorder(out, 3, 3, 3, 3, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return out

orig_panel = add_title(img, "Original Image - Galib")
red_panel = add_title(r_img, "Red Channel")
green_panel = add_title(g_img, "Green Channel")
blue_panel = add_title(b_img, "Blue Channel")

top = np.hstack((orig_panel, red_panel))
bottom = np.hstack((green_panel, blue_panel))
grid = np.vstack((top, bottom))

grid = cv2.copyMakeBorder(grid, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value=(255, 255, 255))

out_path = os.path.join(HERE, "taskA_grid.png")
cv2.imwrite(out_path, grid)

cv2.imshow("Task A Output", grid)
cv2.waitKey(0)
cv2.destroyAllWindows()