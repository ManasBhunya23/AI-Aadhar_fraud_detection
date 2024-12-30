from ultralytics import YOLO

# Load the model
model = YOLO('yolo11n.pt')


# Train the model 
results = model.train(data='my.yaml', epochs=50, imgsz=640)

# Load the trained model
model = YOLO("runs\\detect\\train23\\weights\\best.pt")


# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.box.map  # map50-95
metrics.box.map50  # map50
metrics.box.map75  # map75
metrics.box.maps  # a list contains map50-95 of each category

# Predict with the model
results = model("dataset\\images\\train\\6.jpg")  # predict on an image

# Validate the model
metrics = model.val()
print(metrics.box.map)  # mAP50-95