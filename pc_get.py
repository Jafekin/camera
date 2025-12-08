'''
Author        陈佳辉 1946847867@qq.com
Date          2023-11-22 13:11:47
LastEditTime  2023-12-05 19:55:17
Description   

'''
# '''
# Author        陈佳辉 1946847867@qq.com
# Date          2023-11-22 12:19:19
# LastEditTime  2023-11-23 14:51:33
# Description

# '''
import cv2
import time
import numpy as np

FaceCascade = cv2.CascadeClassifier(
    'D:\\Aproject\\python\\lai\\lbpcascade_frontalface_improved.xml')


def process(src_img):
    # 手机画面水平翻转
    img = cv2.flip(src_img, 1)
    # 将彩色图片转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 检测画面中的人脸
    faces = FaceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )
    # 人脸过滤
    face = face_filter(faces)
    if face is not None:
        # 当前画面有人脸
        (x, y, w, h) = face
        # 在原彩图上绘制矩形
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 4)

    return img


def face_filter(faces):
    '''
    对人脸进行一个过滤
    '''
    if len(faces) == 0:
        return None

    # 目前找的是画面中面积最大的人脸
    max_face = max(faces, key=lambda face: face[2]*face[3])
    (x, y, w, h) = max_face
    if w < 10 or h < 10:
        return None
    return max_face


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
