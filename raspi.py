'''
Author        陈佳辉 1946847867@qq.com
Date          2023-11-22 13:08:46
LastEditTime  2023-11-24 16:29:56
Description   

'''

from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

cap = cv2.VideoCapture(0)
center = []


def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            processed_frame = process(frame)
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='172.6.1.105', port=5000, debug=False)
