import cv2
import numpy as np

img = cv2.imread('../data/sudoku.png')
img_lines1 = img.copy()
img_lines2 = img.copy()

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = img
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))

    cv2.line(img_lines1, (x1, y1), (x2, y2), (0, 0, 255), 1)

lines_p = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength = 50, maxLineGap = 10)

for line in lines_p:
    x1, y1, x2, y2 = line[0]
    cv2.line(img_lines2, (x1, y1), (x2, y2), (0, 255, 0), 1)


imgs = np.hstack([img, img_lines1, img_lines2])
cv2.imshow('Multi_pics', imgs)
#cv2.imshow('Gray', gray)
#cv2.imshow('Edges', edges)
cv2.waitKey(0)


