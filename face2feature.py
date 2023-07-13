import os
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

# # 初始化模型
# model_scrfd = insightface.model_zoo.get_model('F:/deep_learning_projection/code/face_register/buffalo_sc/det_500m.onnx')
# model_w600k = insightface.model_zoo.get_model('F:/deep_learning_projection/code/face_register/buffalo_sc/w600k_mbf.onnx')
# model_scrfd.prepare(ctx_id=0) # 使用GPU 0
# model_w600k.prepare(ctx_id=0)




# 定义检测和识别函数
def detect_and_recognize(img):
    # 检测人脸，返回一个列表，每个元素是一个Face对象，包含人脸的位置，特征
    faces = app.get(img)
    # 如果没有检测到人脸，返回空列表
    if len(faces) == 0:
        return []
    # 否则，返回一个列表，每个元素是一个512维的特征向量
    else:
        return [face.normed_embedding for face in faces]


# 定义计算特征均值的函数
def return_features_mean_personX(personX):
    # 获取personX的子文件夹路径
    personX_path = os.path.join('data/data_faces_from_camera/', personX)
    # 获取personX的所有图片文件名
    personX_files = os.listdir(personX_path)
    # 创建一个空列表，用于存储personX的所有特征向量
    personX_features = []
    # 遍历personX的所有图片文件
    for file in personX_files:
        # 获取图片文件的完整路径
        file_path = os.path.join(personX_path, file)
        # 读取图片文件为numpy数组
        img = cv2.imread(file_path)
        # 调用检测和识别函数，得到图片中的人脸特征向量列表
        features = detect_and_recognize(img)
        print(features)
        # 如果有人脸特征向量，将其添加到personX_features列表中
        if len(features) > 0:
            personX_features.extend(features)
    # 如果personX_features列表不为空，计算其均值，并返回一个numpy数组
    if len(personX_features) > 0:
        return np.mean(personX_features, axis=0)
    # 否则，返回None
    else:
        return None


# 定义写入CSV文件的函数
def write_to_csv(features_dict):
    # 打开CSV文件，如果不存在则创建一个新文件，如果存在则追加内容
    with open('data/features_all.csv', 'a') as f:
        # 遍历特征字典的键值对
        for name, feature in features_dict.items():
            # 如果特征不为空，将姓名和特征转换为字符串，并用逗号分隔，写入一行
            if feature is not None:
                line = name + ',' + ','.join(map(str, feature)) + '\n'
                f.write(line)


if __name__ == '__main__':
    # 创建人脸分析对象
    app = FaceAnalysis(name='my_model_zoo', providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0)
    # 获取data/data_faces_from_camera/ 文件夹下的所有子文件夹名，即人名
    persons = os.listdir('data/data_faces_from_camera/')
    # 创建一个空字典，用于存储每个人名和对应的特征均值
    features_dict = {}
    # 遍历每个人名
    for person in persons:
        # 调用return_features_mean_personX函数，得到该人名对应的特征均值，并存入字典中
        features_dict[person] = return_features_mean_personX(person)
    # 调用write_to_csv函数，将字典中的内容写入CSV文件中
    write_to_csv(features_dict)




# import cv2
# import numpy as np
# import insightface
# from insightface.app import FaceAnalysis
# from insightface.data import get_image as ins_get_image
# import time
# # Method-1, use FaceAnalysis
# app = FaceAnalysis(name='my_model_zoo', providers=['CPUExecutionProvider'], allowed_modules=['detection'])  # enable detection model only
# app.prepare(ctx_id=0, det_size=(640, 640))
#
# img = ins_get_image('t1')
# # img = cv2.imread('./data/data_faces_from_camera/s20201589/s20201589.jpg')
# # start_t = time.time()
# faces = app.get(img)
# # over_t = time.time()
# rimg = app.draw_on(img, faces)
# cv2.imwrite("./t1_output.jpg", rimg)
#
# time = over_t-start_t
# print(time)
# import cv2
# import numpy as np
# import insightface
# from insightface.app import FaceAnalysis
# from insightface.data import get_image as ins_get_image
#
# app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
# app.prepare( det_size=(640, 640))
# img = ins_get_image('t1')
# faces = app.get(img)
# rimg = app.draw_on(img, faces)
# cv2.imwrite("./t1_output.jpg", rimg)
