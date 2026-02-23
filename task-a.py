import os
import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

img_path = os.path.join(HERE, "parrot.jpg")
img = cv2.imread(img_path)
if img is None:
    print("parrot.jpg not found")
    raise SystemExit(1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
b, g, r = cv2.split(img)
edges = cv2.Canny(gray, 100, 200)

gray3 = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
edges3 = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
b3 = cv2.cvtColor(b, cv2.COLOR_GRAY2BGR)
g3 = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
r3 = cv2.cvtColor(r, cv2.COLOR_GRAY2BGR)

W, H = 320, 320
def rs(im): return cv2.resize(im, (W, H))

img_s = rs(img)
gray_s = rs(gray3)
edges_s = rs(edges3)
r_s = rs(r3)
g_s = rs(g3)
b_s = rs(b3)

def put(im, text, color):
    cv2.putText(im, text, (10, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)

put(img_s, "Original", (0, 255, 255))
put(gray_s, "Gray", (255, 255, 255))
put(edges_s, "Edges", (0, 255, 0))
put(r_s, "Red", (0, 0, 255))
put(g_s, "Green", (0, 255, 0))
put(b_s, "Blue", (255, 0, 0))

top = np.hstack([img_s, gray_s, edges_s])
bottom = np.hstack([r_s, g_s, b_s])
grid = np.vstack([top, bottom])

out_path = os.path.join(HERE, "partA_grid.png")
cv2.imwrite(out_path, grid)
cv2.imshow("All Results", grid)
cv2.waitKey(0)
cv2.destroyAllWindows()