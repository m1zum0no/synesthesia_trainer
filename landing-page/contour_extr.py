import cv2
import numpy as np

# Read image
img = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)

# Resize Image
img =  cv2.resize(img, (0,0), fx=0.25, fy=0.25) 

# Initialize output
out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# Median blurring to get rid of the noise; invert image
img = cv2.medianBlur(img, 5)

# Adaptive Treshold
bw = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,15,8)

cv2.imwrite('ed-img.png', bw)
# HoughLinesP
#linesP = cv2.HoughLinesP(bw, 500, np.pi / 180, 50, None, 50, 10)

# Draw Lines
#if linesP is not None:
#    for i in range(0, len(linesP)):
#        l = linesP[i][0]
#        cv2.line(out, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)