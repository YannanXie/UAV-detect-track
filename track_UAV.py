# 跟踪UAV，并根据要求输出txt文件
import os
import glob
from ultralytics import YOLO


# 跟踪UAV(test)
def track_test_UAV(my_img_path, weights_path):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    model = YOLO(weights_path)  # 加载模型

    k = 0
    img_folder = os.listdir(my_img_path)
    sorted_folder = sorted(img_folder)
    for folder_name in sorted_folder:
        results = model.track(
            # source=f"/home/xyn02/Desktop/ultralytics/ultralytics/ultralytics/datasets/UAV/train/videos/{folder_name}.mp4",
            source=f"/home/xyn02/Desktop/ultralytics/ultralytics/ultralytics/datasets/UAV/test/videos/{folder_name}.mp4",
            # show=True,
            save_txt=True,
            max_det=1,
            tracker="bytetrack.yaml")
        k = k + 1
        print(k)


# 清空'ultralytics\datasets\UAV\test\results'下的所有txt文件
def empty_results(result_track):
    sorted_path = sorted(os.listdir(result_track))
    for file_name in sorted_path:
        file_path = os.path.join(result_track, file_name)
        print(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)


# 输入图片，用算法跟踪UAV，输出每一帧图片中UAV的锚框位置（txt文件）
def output_results(my_img_path, runs_track, result_track):
    k = 0
    img_folder = os.listdir(my_img_path)
    sorted_folder = sorted(img_folder)
    file_types = ['*.jpg']
    for folder_name in sorted_folder:
        image_files = []
        image_files.extend(glob.glob(os.path.join(my_img_path, folder_name, file_types[0])))
        image_files = sorted(image_files)
        img_count = len(image_files)
        this_result_track = os.path.join(result_track, f"{folder_name}.txt")
        # print(this_result_track)
        with open(this_result_track, "w") as file:
            file.write('{"res": [')
        # print('{"res": [', end="")
        for i in range(img_count):
            # print(i)
            txt_path = os.path.dirname(image_files[i]).strip().split("/")[5]
            # print(txt_path)
            label_path = os.path.join(runs_track, f"{txt_path}_{i + 1}.txt")
            if os.path.exists(label_path):
                # print("文件存在")
                file = open(label_path, "r")
                # 读取文件内容
                content = file.read()
                # 关闭文件
                file.close()
                # print(content)
                with open(this_result_track, "a") as file:
                    x = content.strip().split(" ")[1]
                    y = content.strip().split(" ")[2]
                    width = content.strip().split(" ")[3]
                    height = content.strip().split(" ")[4]
                    # print(f"[{x},{y},{width},{height}]," if i < 1499 else f"[{x},{y},{width},{height}]", end="")
                    if i < 1499:
                        file.write(f"[{x},{y},{width},{height}],")
                    else:
                        file.write(f"[{x},{y},{width},{height}]")
            else:
                with open(this_result_track, "a") as file:
                    # print("文件不存在")
                    if i < 1499:
                        file.write("[],")
                    else:
                        file.write("[]")
                    # print("[]," if i < 1499 else "[]", end="")
        with open(this_result_track, "a") as file:
            file.write("]}")
        # print("]}")
        k = k + 1
        print(k)
        # if k >= 1:
        #     break
        # else:
        #     print("----------------------------------------------------")


if __name__ == '__main__':
    # initial_train_path = 'ultralytics/datasets/UAV/UAV_detect_track/train'
    initial_test_path = 'ultralytics/datasets/UAV/UAV_detect_track/test'
    # weights_track1 = 'runs/detect/result0524_300/train/weights/best.pt'
    weights_track1 = 'runs/detect/track0525_51/train/weights/best.pt'
    runs_track1 = 'runs/detect/track/labels'
    result_track1 = 'ultralytics/datasets/UAV/test/results'

    # track_test_UAV(initial_train_path, weights_track1)  # 跟踪UAV(train)
    track_test_UAV(initial_test_path, weights_track1)  # 跟踪UAV(test)
    empty_results(result_track1)  # 清空'ultralytics\datasets\UAV\test\results'下的所有txt文件
    output_results(initial_test_path, runs_track1, result_track1)  # 输入图片，用算法跟踪UAV，输出每一帧图片中UAV的锚框位置（txt文件）
