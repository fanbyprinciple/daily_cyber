from ultralytics import YOLO

model = YOLO('yolov8m.pt')

results = model(source=1, show=True, conf=0.4, save=True)

