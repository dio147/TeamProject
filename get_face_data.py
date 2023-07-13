# 导入cv2模块，用于处理图像和视频
import cv2

# 定义一个函数，用于通过摄像头拍摄一张照片并保存到指定路径
def capture_and_save(path):
    # 创建一个VideoCapture对象，参数为0表示使用默认的摄像头
    cap = cv2.VideoCapture(0)
    # 检查是否成功打开摄像头
    if cap.isOpened():
        # 读取一帧图像，返回一个布尔值和一个numpy数组
        ret, frame = cap.read()
        # 检查是否成功读取图像
        if ret:
            # 将图像保存到指定路径，使用cv2.imwrite函数，参数为路径和图像数组
            cv2.imwrite(path, frame)
            # 打印一条提示信息，表示保存成功
            print(f"Image saved to {path}")
        else:
            # 打印一条错误信息，表示读取失败
            print("Failed to read image")
    else:
        # 打印一条错误信息，表示打开失败
        print("Failed to open camera")
    # 释放VideoCapture对象，关闭摄像头
    cap.release()

# 调用函数，传入一个路径作为参数，例如"image.jpg"
capture_and_save("data/data_faces_from_camera/s20201589/s20201589.jpg")
