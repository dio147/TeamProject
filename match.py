# 定义一个函数，计算两个bbox的IoU
def iou(bbox1, bbox2):
    # bbox的格式为[xmin, ymin, xmax, ymax]
    # 计算交集的面积
    inter_xmin = max(bbox1[0], bbox2[0])
    inter_ymin = max(bbox1[1], bbox2[1])
    inter_xmax = min(bbox1[2], bbox2[2])
    inter_ymax = min(bbox1[3], bbox2[3])
    inter_area = max(0, inter_xmax - inter_xmin) * max(0, inter_ymax - inter_ymin)
    # 计算并集的面积
    union_area = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1]) + (bbox2[2] - bbox2[0]) * (
                bbox2[3] - bbox2[1]) - inter_area
    # 计算IoU
    iou = inter_area / union_area
    return iou


# 定义一个函数，对每个body找到最匹配的face
def match(body_boxes, body_labels, face_box, face_label):
    face_boxes = face_box
    face_labels = face_label.copy()
    # 创建一个空列表，存储匹配结果
    matches = []
    # 遍历每个body
    for i in range(len(body_boxes)):
        # 获取当前body的bbox和label
        body_box = body_boxes[i]
        body_label = body_labels[i]
        # 创建一个空字典，存储当前body和所有face的IoU
        ious = {}
        # 遍历每个face
        for j in range(len(face_boxes)):
            # 获取当前face的bbox和label
            face_box = face_boxes[j]
            face_label = face_labels[j]
            # 计算当前body和face的IoU，并存入字典
            ious[j] = iou(body_box, face_box)
        # 对字典按照IoU降序排序，并取出前三个键值对
        top_three = sorted(ious.items(), key=lambda x: x[1], reverse=True)[:3]
        # 创建一个空字典，存储前三个face的y轴差异
        diffs = {}
        # 遍历前三个face
        for k, v in top_three:
            # 获取当前face的bbox和label
            face_box = face_boxes[k]
            face_label = face_labels[k]
            # 计算当前face和body的y轴差异，并存入字典
            diffs[k] = abs(face_box[1] - body_box[1])
        # 对字典按照y轴差异升序排序，并取出第一个键值对
        if diffs:  # 如果字典不为空
            best_match = sorted(diffs.items(), key=lambda x: x[1])[0]
            # 获取最匹配的face的索引和label
            match_index = best_match[0]
            match_label = face_labels[match_index]
            # 将当前body的label和最匹配的face的label组成一个元组，并添加到匹配结果列表中
            matches.append((match_label, body_label))
            face_boxes.pop(match_index)
            face_labels.pop(match_index)
        else:  # 如果字典为空
            matches.append(("unknown", body_label))  # 给当前body一个默认的匹配结果

    # 返回匹配结果列表
    return matches


if __name__ == '__main__':
    students_body_boxes = [[100, 200, 300, 400], [150, 250, 350, 450], [200, 300, 400, 500]]
    # students_body_boxes = []
    students_body_labels = ["听讲", "听讲", "分心"]
    students_face_boxes = [[120, 210, 280, 290], [160, 260, 340, 360]]
    # students_face_boxes = []
    students_face_labels = ["s20201589", "s20201583"]

    matches = match(students_body_boxes, students_body_labels, students_face_boxes, students_face_labels)
    print(matches)
    print(students_face_labels)

