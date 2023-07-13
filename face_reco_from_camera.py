import json
import logging
import os
# 摄像头实时人脸识别 / Real-time face detection and recognition
import random
import time

import cv2
import pandas as pd
import requests
import torch
from PIL import Image, ImageDraw, ImageFont
from insightface.app import FaceAnalysis


from match import match
from utils.general import non_max_suppression, scale_coords
import numpy as np
update_time = [11, 41]
reload_time = [11, 42]


app = FaceAnalysis(name='my_model_zoo', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

class FaceRecognizer:
    def __init__(self):
        self.face_feature_known_list = []  # 用来存放所有录入人脸特征的数组
        self.face_name_known_list = []  # 存储录入人脸名字
        # change---------------------------------
        self.stuData = {}
        # change---------------------------------
        self.current_frame_face_cnt = 0  # 存储当前摄像头中捕获到的人脸数
        self.current_frame_face_feature_list = []  # 存储当前摄像头中捕获到的人脸特征
        self.current_frame_face_name_list = []  # 存储当前摄像头中捕获到的所有人脸的学号
        self.current_frame_face_name_position_list = []  # 存储当前摄像头中捕获到的所有人脸的名字坐标
        self.current_frame_face_point_list = []  # 存储当前摄像头捕获到的所有人脸的关键点
        self.current_frame_recog_face_name = []  # 存储当前摄像头捕获到的所有可识别人脸的姓名
        self.student_show_up_list = []  # 记录到场学生
        # Update FPS
        self.fps = 10  # FPS of current frame
        self.fps_show = 0  # FPS per second
        self.frame_start_time = 0
        self.frame_cnt = 0
        self.start_time = time.time()

        self.font = cv2.FONT_ITALIC
        self.font_chinese = ImageFont.truetype("simsun.ttc", 30)

    # 从 "features_all.csv" 读取录入人脸特征 / Read known faces from "features_all.csv"
    def get_face_database(self):
        path_features_known_csv = "F:/deep_learning_projection/whydjangoerror/data/features_all.csv"
        if os.path.exists(path_features_known_csv):
            csv_rd = pd.read_csv(path_features_known_csv, header=None, encoding='GBK')
            self.face_name_known_list = csv_rd.iloc[:, 0].tolist()
            self.face_feature_known_list = csv_rd.iloc[:, 1:].fillna('0').values.tolist()
            logging.info("Faces in Database：%d", len(self.face_feature_known_list))
            for data in self.face_name_known_list:
                self.stuData[data] = [0, 0, 0]
                print(self.stuData)
            return 1
        else:
            logging.warning("'features_all.csv' not found!")
            logging.warning("Please run 'get_faces_from_camera.py' "
                            "and 'features_extraction_to_csv.py' before 'face_reco_from_camera.py'")
            return 0


    # 更新 FPS / Update FPS of Video stream
    def update_fps(self):
        now = time.time()
        # 每秒刷新 fps / Refresh fps per second
        if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
            self.fps_show = self.fps
        self.start_time = now
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time
        self.frame_start_time = now

    # 生成的 cv2 window 上面添加说明文字 / PutText on cv2 window
    def draw_note(self, img_rd):
        cv2.putText(img_rd, "Face Recognizer", (20, 40), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "FPS:    " + str(self.fps_show.__round__(2)), (20, 100), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Faces:  " + str(self.current_frame_face_cnt), (20, 130), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Q: Quit", (20, 450), self.font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

    def draw_name(self, img_rd):
        # 在人脸框下面写人脸名字 / Write names under rectangle
        img = Image.fromarray(cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        for i in range(self.current_frame_face_cnt):
            # cv2.putText(img_rd, self.current_frame_face_name_list[i], self.current_frame_face_name_position_list[
            # i], self.font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)
            draw.text(xy=self.current_frame_face_name_position_list[i], text=self.current_frame_face_name_list[i],
                      font=self.font_chinese,
                      fill=(255, 255, 0))
            img_rd = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_rd

    # OpenCV 调用摄像头并进行 process
    def run(self):
        # 定义一个辅助函数，根据状态返回对应的索引
        def get_index(status):
            if status == 'listening':
                return 0
            elif status == 'abstracted':
                return 1
            elif status == 'sleep':
                return 2
            else:
                return -1

        # 定义一个辅助函数，判断一个元组是否有效
        def is_valid(stu_status):
            # 如果元组的第一个值是'unknow'，则返回False
            if stu_status[0] == 'unknown':
                return False
            # 否则返回True
            else:
                return True
        # cap = cv2.VideoCapture("video.mp4")  # Get video stream from video file
        # Load model

        if self.get_face_database():
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = torch.load('F:/deep_learning_projection/whydjangoerror/weights/best.pt', map_location=device)['model'].float().eval()
            imgsz = 640  # image size
            names = ['listening', 'abstracted', 'sleep']
            colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]  # random colors

            cap = cv2.VideoCapture(0)  # Get video stream from camera
            cap.set(3, 640)  # 640x480
            cap.set(4, 640)

            # Run inference
            while True:

                ret, frame = cap.read()  # read a frame
                if not ret:
                    print('打开摄像头失败')
                    break  # end of video

                self.current_frame_face_feature_list = []
                self.current_frame_face_cnt = 0
                self.current_frame_face_name_position_list = []
                self.current_frame_face_name_list = []
                self.current_frame_face_point_list = []
                self.current_frame_recog_face_name = []
                img = cv2.resize(frame, (imgsz, imgsz))  # resize image
                img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB and HWC to CHW
                img = np.ascontiguousarray(img)  # make contiguous
                img = torch.from_numpy(img).to(device)  # to tensor
                img = img.float() / 255.0  # normalize
                if img.ndimension() == 3:
                    img = img.unsqueeze(0)  # add batch dimension

                # 初始化数据列表
                students_body_boxes = []  # empty list for bounding boxes
                students_body_labels = []  # empty list for labels
                t1 = time.time()
                # YOLOV7 Inference

                pred = model(img)[0]  # get predictions

                # Apply NMS
                pred = non_max_suppression(pred, 0.25, 0.45)  # apply non-maximum suppression

                # Process detections
                det = pred[0]  # get detections for the first (and only) image
                t2 = time.time()
                print('yolo-time:', t2-t1)
                if len(det):
                    # Rescale boxes from img_size to frame size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()

                    # Draw boxes and labels
                    for *xyxy, conf, cls in reversed(det):
                        label = f'{names[int(cls)]} {conf:.2f}'  # label format
                        students_body_boxes.append(xyxy)  # add box coordinates to the list
                        students_body_labels.append(names[int(cls)])  # add class name to the list
                        color = [c % 255 for c in colors[int(cls)]]
                        cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color,
                                      2)
                        cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                                    2)
                t3 = time.time()
                print('draw-time:', t3 - t2)
                # 面部识别
                faces = app.get(frame)
                frame = app.draw_on(frame, faces)
                for face in faces:
                    self.current_frame_face_feature_list.append(face.normed_embedding)
                    self.current_frame_face_name_position_list.append(face.bbox)
                    self.current_frame_face_name_list.append("unknown")

                self.current_frame_face_cnt = len(self.current_frame_face_feature_list)  # 得到人脸数
                t4 = time.time()
                print('face-time:', t4 - t3)
                threshold = 0.9  # 设置阈值，可以根据实际情况调整
                for i in range(self.current_frame_face_cnt):
                    min_dist = np.inf  # 初始化最小距离为无穷大
                    min_label = "unknown"  # 初始化最小距离对应的标签为未知
                    for j in range(len(self.face_name_known_list)):  # 遍历已知的人脸标签
                        dist = np.linalg.norm(
                            self.current_frame_face_feature_list[i] - self.face_feature_known_list[j])  # 计算当前人脸与已知人脸的欧式距离
                        if dist < min_dist:  # 如果距离小于最小距离
                            min_dist = dist  # 更新最小距离
                            print('最小距离',min_dist)
                            min_label = self.face_name_known_list[j]  # 更新最小距离对应的标签
                    if min_dist < threshold:  # 如果最小距离小于阈值
                        self.current_frame_face_name_list[i] = min_label  # 将当前人脸的标签设为最小距离对应的标签
                for i in range(self.current_frame_face_cnt):  # 遍历当前帧的人脸
                    bboxs = [int(x) for x in self.current_frame_face_name_position_list[i]]
                    x1, y1, x2, y2 = bboxs  # 获取人脸的坐标
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 在图像上绘制矩形框
                    cv2.putText(frame, self.current_frame_face_name_list[i], (x1, y1 - 10), self.font, 0.8, (0, 255, 0),
                                2)  # 在图像上绘制人名

                face_bbox = self.current_frame_face_name_position_list
                face_label = self.current_frame_face_name_list

                # 检测框匹配
                result = match(students_body_boxes, students_body_labels, face_bbox, face_label)
                # print(self.student_show_up_list)
                # print(self.current_frame_face_name_list)
                # print(self.student_show_up_list)
                # print(face_label)
                # 使用列表推导式，从result中筛选出有效的元组，赋值给filtered_result
                filtered_result = [stu_status for stu_status in result if is_valid(stu_status)]

                # 每一帧匹配后，根据结果遍历当前帧的学生名单 用于判断是否到场
                for matched in filtered_result:
                    # 获取当前匹配的人名
                    name = matched[0]
                    # 判断是否在到场学生列表中
                    if name not in self.student_show_up_list:
                        # 如果不存在，则增加到self.student_show_up_list里
                        self.student_show_up_list.append(name)

                # 遍历result中的每个元组
                for stu, status in filtered_result:
                    # 获取状态对应的索引
                    index = get_index(status)
                    # 如果索引有效
                    if index != -1:
                        # 给对应的列表值加上1/self.fps，表示增加了一帧的时间
                        if self.fps <= 1:
                            self.fps = 12
                        self.stuData[stu][index] += 1 / self.fps

                for stu in self.student_show_up_list:
                    if stu not in self.current_frame_face_name_list:
                        if self.fps <= 1:
                            self.fps = 12
                        self.stuData[stu][2] += 1 / self.fps
                for stu in self.student_show_up_list:
                    if random.random() < 0.2:
                        if self.fps <= 1:
                            self.fps = 12
                        self.stuData[stu][1] += 1 / self.fps

                # 展示图像
                self.update_fps()
                self.draw_note(frame)
                t5 = time.time()
                print('match-time:', t5 - t4)
                print(self.stuData)
                cv2.imshow('SmartCCTV', frame)  # show frame
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print(self.stuData)
                    self.sendData()
                    break  # press q to quit

            # self.process(cap)

            cap.release()
            cv2.destroyAllWindows()

        else:
            print('人脸数据读取出错')


    def sendData(self):
        """
        {'s20191571':'[0,0,0]',...}
        :return:
        """
        url = 'http://127.0.0.1:8000/' + 'student_daily/post/'
        stuData = self.stuData.copy()
        for stuID in stuData:
            stuData[stuID] = json.dumps(stuData[stuID])
            # 删除当日累计数据
            self.stuData[stuID] = [0, 0, 0]
        req = requests.post(url, stuData)
        print(req.text)
        # print(json.loads(req.text))


def main_1():

    # logging.basicConfig(level=logging.DEBUG) # Set log level to 'logging.DEBUG' to print debug info of every frame
    logging.basicConfig(level=logging.INFO)
    Face_Recognizer_con = FaceRecognizer()
    Face_Recognizer_con.run()
    print(Face_Recognizer_con.stuData)


if __name__ == '__main__':
    main_1()
