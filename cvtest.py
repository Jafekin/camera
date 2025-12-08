# '''
# Author        陈佳辉 1946847867@qq.com
# Date          2023-11-22 12:19:19
# LastEditTime  2023-11-23 14:51:33
# Description

# '''
import cv2
import numpy as np


def process(src_img):
    dst_img = src_img.copy()
    temp_img = src_img.copy()
    temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)  # 将图像转换为灰度
    temp_img = cv2.GaussianBlur(temp_img, (3, 3), 0, 0)  # 对灰度图像进行高斯滤波
    _, temp_img = cv2.threshold(temp_img, 230, 255, cv2.THRESH_BINARY)  # 二值化图像

    contours, hierarcy = cv2.findContours(
        temp_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # 寻找轮廓
    boxes = []

    for contour in contours:
        if len(contour) >= 5:  # 至少5个点才能拟合椭圆
            box = cv2.fitEllipse(contour)
            boxes.append(box)

    max_index = 0
    max_area = 0

    for i, box in enumerate(boxes):
        center, size, angle = box

        if not (np.isnan(center[0]) or np.isnan(center[1]) or np.isnan(size[0]) or np.isnan(size[1])):
            size = (int(size[0]), int(size[1]))

            if size[1] > 15 and size[0] > 15 and size[1] * size[0] > max_area:
                max_area = size[1] * size[0]
                max_index = i

    if max_area != 0:  # 绘制中心十字
        center, size, angle = boxes[max_index]

        if not (np.isnan(center[0]) or np.isnan(center[1]) or np.isnan(size[0]) or np.isnan(size[1])):
            center = (int(center[0]), int(center[1]))
            size = (int(size[0]), int(size[1]))

            cv2.line(dst_img, (center[0], center[1] - 6),
                     (center[0], center[1] + 6), (0, 0, 255), 2, 8)
            cv2.line(dst_img, (center[0] - 6, center[1]),
                     (center[0] + 6, center[1]), (0, 0, 255), 2, 8)
            cv2.ellipse(dst_img, (center, size, angle), (0, 255, 0), 1, 8)

    return dst_img


def main():
    camera_index = 0
    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        print("打开摄像头失败")
        return -1

    while True:
        ret, cache = camera.read()
        cv2.imshow("test", process(cache))

        if cv2.waitKey(20) & 0xFF == 27:
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
