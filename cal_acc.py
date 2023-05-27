import os
import glob
from decimal import Decimal, getcontext


def calculate_IoU(box1, box2):
    '''
    两个框（二维）的 IoU 计算
    注意：边框以左上为原点
    box:[x1,y1,x2,y2],依次为左上右下坐标
    '''
    h = max(0, min(box1[2], box2[2]) - max(box1[0], box2[0]))
    w = max(0, min(box1[3], box2[3]) - max(box1[1], box2[1]))
    area_box1 = ((box1[2] - box1[0]) * (box1[3] - box1[1]))
    area_box2 = ((box2[2] - box2[0]) * (box2[3] - box2[1]))
    inter = w * h
    union = area_box1 + area_box2 - inter
    iou = inter / union
    return iou


def calculate_acc(initial_path, pred_path, real_path):
    getcontext().prec = 10  # 设置精度为10位小数
    k = 0
    img_folder = os.listdir(initial_path)
    sorted_folder = sorted(img_folder)
    file_types = ['*.jpg']
    T = 0  # 总帧数
    T_pred = 0  # 目标在预测标签中的存在帧数
    T_real = 0  # 目标在真实标签中的存在帧数
    numerator_former = 0
    numerator_latter = 0
    for folder_name in sorted_folder:
        # print(folder_name)
        image_files = []
        image_files.extend(glob.glob(os.path.join(initial_path, folder_name, file_types[0])))
        image_files = sorted(image_files)
        img_count = len(image_files)
        T += img_count
        for i in range(img_count):
            pred_i_path = os.path.join(pred_path, f"{folder_name}_{i + 1}.txt")
            real_i_path = os.path.join(real_path, f"{folder_name}__{i + 1:06d}.txt")
            # print(pred_i_path)
            # print(real_i_path)
            # 判断预测框是否可见
            if os.path.isfile(pred_i_path):
                # print(f"{pred_i_path}文件存在")
                T_pred += 1
                # print(T_pred)
                file = open(pred_i_path, "r")
                pred_content = file.read()
                file.close()
                pred_x = Decimal(pred_content.strip().split(" ")[1])
                pred_y = Decimal(pred_content.strip().split(" ")[2])
                pred_width = Decimal(pred_content.strip().split(" ")[3])
                pred_height = Decimal(pred_content.strip().split(" ")[4])
                pred_box = [pred_x, pred_y, pred_width, pred_height]
                p_i = Decimal('0')
            else:
                # print(f"{pred_i_path}文件不存在")
                pred_box = [Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0')]
                p_i = Decimal('1')
            # 判断真实框是否可见
            if os.path.getsize(real_i_path) == 0:
                delta_v_i = Decimal('0')
                real_box = [Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0')]
            else:
                delta_v_i = Decimal('1')
                T_real += 1
                file = open(real_i_path, "r")
                real_content = file.read()
                file.close()
                real_x = Decimal(real_content.strip().split(" ")[1])
                real_y = Decimal(real_content.strip().split(" ")[2])
                real_width = Decimal(real_content.strip().split(" ")[3])
                real_height = Decimal(real_content.strip().split(" ")[4])
                real_box = [real_x, real_y, real_width, real_height]

            if pred_box == [Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0')] or real_box == [Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0')]:
                IoU_i = Decimal('0')
            else:
                IoU_i = calculate_IoU(pred_box, real_box)

            numerator_former += IoU_i * delta_v_i + p_i * (1 - delta_v_i)
            numerator_latter += p_i * delta_v_i

        k = k + 1
        print(k)
        # if k >= 1:
        #     break
        # else:
        #     print("----------------------------------------------------")
    print(T)
    print(T_pred)
    print(T_real)
    acc = numerator_former / Decimal(T) + Decimal('0.2') * ((numerator_latter / Decimal(T_real)) ** Decimal('0.3'))
    print(acc)


if __name__ == '__main__':
    initial_train_path = '/home/xyn02/Desktop/ultralytics/ultralytics/ultralytics/datasets/UAV/UAV_detect_track/train'
    pred_txt_path = '/home/xyn02/Desktop/ultralytics/ultralytics/runs/detect/track/labels'
    real_txt_path = '/home/xyn02/Desktop/ultralytics/ultralytics/ultralytics/datasets/UAV/train_initial/labels'
    calculate_acc(initial_train_path, pred_txt_path, real_txt_path)

