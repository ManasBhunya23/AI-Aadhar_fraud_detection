from ultralytics import YOLO

# Load the model
model = YOLO('yolo11n-cls.pt')

# Train the model 
results = model.train(data='dataset', epochs=2, imgsz=256, batch=8)

# Load the trained model
model = YOLO("runs\\classify\\train\\weights\\best.pt")


# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.top1  # top1 accuracy
metrics.top5  # top5 accuracys

# Predict with the model
results = model("aadhar sample.jpg") 

for result in results:
    predicted_class_index =result.probs.top1

    predicted_class = result.names[predicted_class_index]
    print(f'The image is classified as: {predicted_class}')