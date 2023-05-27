from ultralytics import YOLO
import os
from PIL import Image

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 加载模型
# model = YOLO("UAV.yaml")  # 从头开始构建新模型
model = YOLO("yolov8n.pt")  # 加载预训练模型（建议用于训练）
# model = YOLO("/home/xyn02/Desktop/ultralytics/ultralytics/runs/detect/result0521_100/train/weights/best.pt")
# model = YOLO("/home/xyn02/Desktop/ultralytics/ultralytics/runs/detect/result0524_300/train/weights/best.pt")

# 使用模型
model.train(data="UAV.yaml", epochs=300)  # 训练模型
metrics = model.val()  # 在验证集上评估模型性能
success = model.export(format="onnx")  # 将模型导出为 ONNX 格式