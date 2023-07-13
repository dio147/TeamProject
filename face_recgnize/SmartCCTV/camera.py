import random

import numpy as np
# import torch
# import cv2
# from utils.general import non_max_suppression, scale_coords
import cv2

stop_flag = False
# imgsz = 640  # image size
# names = ['listening', 'look down', 'sleep']
# colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]  # random colors
def close_mo(cap):
    cap.release()  # 释放摄像头资源
    cv2.destroyAllWindows()  # 销毁窗口
    global stop_flag
    stop_flag = False

def open_camera():
    # Set webcam
    cap = cv2.VideoCapture(0)  # open webcam 0
    # Run inference
    while True:
        ret, frame = cap.read()  # read a frame
        if not ret:
            break  # end of video
        #
        # # img = cv2.resize(frame, (imgsz, imgsz))  # resize image
        # img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB and HWC to CHW
        # img = np.ascontiguousarray(img)  # make contiguous
        # img = torch.from_numpy(img).to(device)  # to tensor
        # img = img.float() / 255.0  # normalize
        # if img.ndimension() == 3:
        #     img = img.unsqueeze(0)  # add batch dimension
        #
        # # Inference
        # pred = model(img)[0]  # get predictions
        #
        # # Apply NMS
        # pred = non_max_suppression(pred, 0.25, 0.45)  # apply non-maximum suppression
        #
        # # Process detections
        # det = pred[0]  # get detections for the first (and only) image
        # if len(det):
        #     # Rescale boxes from img_size to frame size
        #     det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
        #
        #     # Draw boxes and labels
        #     for *xyxy, conf, cls in reversed(det):
        #         label = f'{names[int(cls)]} {conf:.2f}'  # label format
        #         color = [c % 255 for c in colors[int(cls)]] # color format
        #         cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)  # draw rectangle
        #         cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
        #                     2)  # draw text

        cv2.imshow('frame', frame)  # show frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # press q to quit
    return cap

def close_camera():
    global stop_flag  # 引用全局变量
    stop_flag = True  # 设置关闭标志


if __name__ == '__main__':
    cap = open_camera()
    close_mo(cap)
