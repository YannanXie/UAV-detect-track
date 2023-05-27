import os
import glob
import random
import shutil
from PIL import Image
import math
import cv2


def read_train_json(img_path):
    k = 0
    file_types = ['*.jpg']
    label_path = 'ultralytics/datasets/UAV/train_initial/labels'
    file_list = os.listdir(img_path)
    sorted_list = sorted(file_list)
    for folder_name in sorted_list:
        # print(folder_name)
        image_files = []
        image_files.extend(glob.glob(os.path.join(img_path, folder_name, file_types[0])))
        image_files = sorted(image_files)
        # 构造.json文件的完整路径
        json_path = os.path.join(img_path, folder_name, 'IR_label.json')
        # 检查文件是否存在并且是一个文件而不是目录
        if os.path.isfile(json_path):
            # 处理.json文件，例如读取其中的数据
            with open(json_path, 'r') as f:
                json_data = f.read()
                json_data_count = json_data.count("[") - 2
                for i in range(json_data_count):
                    verify_last = json_data.strip().split('[')[1].split(', ')
                    if i == json_data_count - 1:
                        whether_exist = verify_last[i].strip(']')
                    else:
                        whether_exist = verify_last[i]
                    exist_position = []
                    if whether_exist == '1':
                        if i == json_data_count - 1:
                            for j in range(4):
                                tmp = json_data.strip().split('[')[i + 3].strip(']]}').split(', ')
                                exist_position.append(tmp[j])
                            # print(exist_position)
                        else:
                            for j in range(4):
                                tmp = json_data.strip().split('[')[i + 3].strip('], ').split(', ')
                                exist_position.append(tmp[j])
                            # print(exist_position)
                    else:
                        exist_position = [0, 0, 0, 0]
                        # print(exist_position)

                    img = Image.open(image_files[i])
                    width, height = img.size
                    # print(width, height)
                    # label_path =
                    # label_path = image_files[i].replace("images", "labels").strip().split("\\")
                    # file_path = os.path.join(label_path[0], label_path[1], label_path[2], label_path[3], label_path[4],
                    #                          label_path[5])
                    # if not os.path.exists(file_path):
                    #     os.makedirs(file_path)
                    # label_path = os.path.join(file_path, label_path[6]).strip('.jpg') + '.txt'
                    # print(label_path)
                    # print(image_files[i])

                    one_img_name = image_files[i].strip().split("/")[6]
                    one_label_path = f"{label_path}/{folder_name}__{one_img_name}"
                    one_label_path = one_label_path.strip('.jpg') + '.txt'
                    # print(one_label_path)
                    with open(one_label_path, "w") as file:
                        # < object -class -id > < x > < y > < width > < height > 归一化
                        if exist_position != [0, 0, 0, 0]:
                            file.write("0 " + str(int(exist_position[0]) / width) + " " + str(
                                int(exist_position[1]) / height) + " " + str(
                                int(exist_position[2]) / width) + " " + str(int(exist_position[3]) / height))
        k = k + 1
        print(k)
        # if k >= 1:
        #     break
        # else:
        #     print("----------------------------------------------------")


def put_img_together(img_path):
    k = 0
    file_types = ['*.jpg']
    output_img_path = 'ultralytics/datasets/UAV/train_initial/images'
    for folder_name in os.listdir(img_path):
        image_files = []
        image_files.extend(glob.glob(os.path.join(img_path, folder_name, file_types[0])))
        json_path = os.path.join(img_path, folder_name, 'IR_label.json')
        # 检查文件是否存在并且是一个文件而不是目录
        if os.path.isfile(json_path):
            # 处理.json文件，例如读取其中的数据
            with open(json_path, 'r') as f:
                json_data = f.read()
                json_data_count = json_data.count("[") - 2
                for i in range(json_data_count):
                    # print(image_files[i])
                    source_file_folder = image_files[i].strip().split("/")[5]
                    source_file_name = image_files[i].strip().split("/")[6]
                    destination_folder = f"{output_img_path}/{source_file_folder}__{source_file_name}"
                    shutil.copy2(image_files[i], destination_folder)
        k = k + 1
        print(k)
        # if k >= 1:
        #     break
        # else:
        #     print("----------------------------------------------------")


def random_sample_files(image_folder, txt_folder, train_ratio):
    sample_size = math.floor(train_ratio * 172626)
    image_files = os.listdir(image_folder)
    txt_files = os.listdir(txt_folder)
    assert len(image_files) == len(txt_files)

    sample_files = random.sample(image_files, sample_size)
    train_image_folder = 'ultralytics/datasets/UAV/train/images'
    train_txt_folder = 'ultralytics/datasets/UAV/train/labels'
    val_image_folder = 'ultralytics/datasets/UAV/val/images'
    val_txt_folder = 'ultralytics/datasets/UAV/val/labels'

    k = 0
    for filename in sample_files:
        source_image = os.path.join(image_folder, filename)
        destination_image = os.path.join(train_image_folder, filename)
        shutil.copy2(source_image, destination_image)

        txt_filename = os.path.splitext(filename)[0] + ".txt"
        source_txt = os.path.join(txt_folder, txt_filename)
        destination_txt = os.path.join(train_txt_folder, txt_filename)
        shutil.copy2(source_txt, destination_txt)

        # print(f"已复制文件: {source_image} -> {destination_image}")
        # print(f"已复制文件: {source_txt} -> {destination_txt}")
        k = k + 1
        print(k)
        # if k >= 2:
        #     break

    k = 0
    for filename in image_files:
        if filename not in sample_files:
            source_image = os.path.join(image_folder, filename)
            destination_image = os.path.join(val_image_folder, filename)
            shutil.copy2(source_image, destination_image)

            txt_filename = os.path.splitext(filename)[0] + ".txt"
            source_txt = os.path.join(txt_folder, txt_filename)
            destination_txt = os.path.join(val_txt_folder, txt_filename)
            shutil.copy2(source_txt, destination_txt)

            # print(f"已复制文件: {source_image} -> {destination_image}")
            # print(f"已复制文件: {source_txt} -> {destination_txt}")
            k = k + 1
            print(k)


# 整合视频流
def create_video(my_img_path):
    k = 0
    img_folder = os.listdir(my_img_path)
    sorted_folder = sorted(img_folder)
    for folder_name in sorted_folder:
        first_img_path = os.path.join(my_img_path, folder_name, '000001.jpg')
        # print(folder_name)
        # print(first_img_path)
        # 设置图像尺寸和帧速率
        first_img = Image.open(first_img_path)
        width, height = first_img.size
        fps = 30
        # 创建视频编码器
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        # print(folder_name)
        # video_path = f"ultralytics/datasets/UAV/test/videos/{folder_name}.mp4"
        video_path = f"ultralytics/datasets/UAV/train/videos/{folder_name}.mp4"
        # print(video_path)
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
        # 获取图像文件列表并按文件名排序
        img_dir = os.path.join(my_img_path, folder_name)
        img_files = sorted([f for f in os.listdir(img_dir) if f.endswith(".jpg")])
        # 遍历图像文件并写入视频流
        for img_file in img_files:
            img_path = os.path.join(img_dir, img_file)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (width, height))
            out.write(img)
        # 释放资源
        out.release()

        k = k + 1
        print(k)
        # if k >= 1:
        #     break
        # else:
        #     print("----------------------------------------------------")


if __name__ == '__main__':
    # 1.
    # initial_train_path = 'ultralytics/datasets/UAV/UAV_detect_track/train'
    # put_img_together(initial_train_path)

    # 2.
    # initial_train_path = 'ultralytics/datasets/UAV/UAV_detect_track/train'
    # read_train_json(initial_train_path)

    # 3.
    # image_folder = 'ultralytics/datasets/UAV/train_initial/images'
    # txt_folder = 'ultralytics/datasets/UAV/train_initial/labels'
    # train_ratio = 0.85
    # random_sample_files(image_folder, txt_folder, train_ratio)

    # 整合test视频流
    # initial_test_path = 'ultralytics/datasets/UAV/UAV_detect_track/test'
    # create_video(initial_test_path)

    # 整合train视频流
    initial_train_path = 'ultralytics/datasets/UAV/UAV_detect_track/train'
    create_video(initial_train_path)


