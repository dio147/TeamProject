import cv2 as cv

# 以灰度图的形式读取图像
img = cv.imread('testImg.png', 0)
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", img)
cv.waitKey(0)
cv.destroyAllWindows()
