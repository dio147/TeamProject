import random

import numpy as np
import torch
import cv2
from utils.general import non_max_suppression, scale_coords
import cv2
# cap = cv2.VideoCapture('test_vedio.mp4')  # open webcam 0
# ret, frame = cap.read()  # read the first frame
# FPS = cap.get(cv2.CAP_PROP_FPS)  # get the frame rate
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # set the video codec
# out = cv2.VideoWriter('resized_video.mp4', fourcc, FPS, (640, 640))  # create a video writer object
# while ret:  # loop until the end of the video
#     resized_frame = cv2.resize(frame, (640, 640))  # resize the current frame
#     out.write(resized_frame)  # write the resized frame to the output video
#     ret, frame = cap.read()  # read the next frame
# cap.release()  # release the input video object
# out.release()  # release the output video object

# Load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load('weights/best.pt', map_location=device)['model'].float().eval()
imgsz = 640  # image size
names = ['listening', 'look down', 'sleep']
colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]  # random colors

# Set webcam
cap = cv2.VideoCapture(0)  # open webcam 0
cap = cv2.VideoCapture('resized_video.mp4')
cap.set(3, 640)  # set width
cap.set(4, 640)  # set height



# Run inference
while True:
    ret, frame = cap.read()  # read a frame
    if not ret:
        break  # end of video

    img = cv2.resize(frame, (imgsz, imgsz))  # resize image
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB and HWC to CHW
    img = np.ascontiguousarray(img)  # make contiguous
    img = torch.from_numpy(img).to(device)  # to tensor
    img = img.float() / 255.0  # normalize
    if img.ndimension() == 3:
        img = img.unsqueeze(0)  # add batch dimension

    # Inference
    pred = model(img)[0]  # get predictions

    # Apply NMS
    pred = non_max_suppression(pred, 0.25, 0.45)  # apply non-maximum suppression

    # Process detections
    det = pred[0]  # get detections for the first (and only) image
    if len(det):
        # Rescale boxes from img_size to frame size
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()

        # Draw boxes and labels
        for *xyxy, conf, cls in reversed(det):
            label = f'{names[int(cls)]} {conf:.2f}'  # label format
            color = [c % 255 for c in colors[int(cls)]] # color format
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)  # draw rectangle
            cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                        2)  # draw text

    cv2.imshow('frame', frame)  # show frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # press q to quit

cap.release()  # release webcamdd
cv2.destroyAllWindows()  # destroy windows

