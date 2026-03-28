import cv2
import numpy as np

# 1) Read image
img = cv2.imread("parrot.jpg")
if img is None:
    print("Image load hoy nai")
    raise SystemExit

# 2) Create outputs
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
b, g, r = cv2.split(img)
edges = cv2.Canny(gray, 100, 200)

# 3) Convert all to 3-channel for stacking
gray3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
edges3 = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
b3 = cv2.cvtColor(b, cv2.COLOR_GRAY2BGR)
g3 = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
r3 = cv2.cvtColor(r, cv2.COLOR_GRAY2BGR)

# 4) Resize all to same size
W, H = 320, 320
def rs(im): return cv2.resize(im, (W, H))

img_s = rs(img)
gray_s = rs(gray3)
edges_s = rs(edges3)
r_s = rs(r3)
g_s = rs(g3)
b_s = rs(b3)

# 5) Put labels (BGR colors)
def put(im, text, color):
    cv2.putText(im, text, (10, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)
    return im

put(img_s,   "Original", (0, 255, 255))
put(gray_s,  "Gray",     (255, 255, 255))
put(edges_s, "Edges",    (0, 255, 0))
put(r_s,     "Red",      (0, 0, 255))
put(g_s,     "Green",    (0, 255, 0))
put(b_s,     "Blue",     (255, 0, 0))

# 6) Make 2x3 grid (ONLY ONCE)
top = np.hstack([img_s, gray_s, edges_s])
bottom = np.hstack([r_s, g_s, b_s])
grid = np.vstack([top, bottom])

# 7) Show + Save
cv2.imshow("All Results", grid)
cv2.imwrite("partA_grid.png", grid)

cv2.waitKey(0)
cv2.destroyAllWindows()