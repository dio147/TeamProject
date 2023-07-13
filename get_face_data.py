import cv2
import os

def capture_and_save(student_id):
    # 定义保存路径
    save_dir = f"data/data_faces_from_camera/{student_id}"
    save_path = f"{save_dir}/{student_id}.jpg"
    # 如果保存路径不存在，则创建
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # 创建一个VideoCapture对象，参数为0表示使用默认的摄像头
    cap = cv2.VideoCapture(0)
    # 检查是否成功打开摄像头
    if cap.isOpened():
        while True:
            # 读取一帧图像，返回一个布尔值和一个numpy数组
            ret, frame = cap.read()
            # 检查是否成功读取图像
            if ret:
                # 显示图像
                cv2.imshow("Press 'w' to capture", frame)
                # 等待用户按键
                key = cv2.waitKey(1)
                # 如果用户按下'w'键
                if key == ord('w'):
                    # 将图像保存到指定路径，使用cv2.imwrite函数，参数为路径和图像数组
                    cv2.imwrite(save_path, frame)
                    # 打印一条提示信息，表示保存成功
                    print(f"Image saved to {save_path}")
                    break
            else:
                # 打印一条错误信息，表示读取失败
                print("Failed to read image")
                break
    else:
        # 打印一条错误信息，表示打开失败
        print("Failed to open camera")
    # 释放VideoCapture对象，关闭摄像头
    cap.release()
    cv2.destroyAllWindows()

# 获取用户输入的学号
student_id = input("Please enter the student ID: ")
# 调用函数，传入学号作为参数
capture_and_save(student_id)
