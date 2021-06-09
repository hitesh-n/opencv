import cv2 as cv
import sys
img = cv.imread("/Users/hitesh/Downloads/<image_name>")
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img)
cv.imwrite("<New file name>", img)
