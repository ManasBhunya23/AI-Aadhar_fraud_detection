from ultralytics import YOLO
import easyocr
import cv2

# Load the trained YOLO model
model = YOLO("runs\\detect\\train3\\weights\\best.pt")

# Load EasyOCR Reader
reader = easyocr.Reader(['en'])  # Initialize EasyOCR with English language

# Predict with YOLO
image_path = "dataset\\images\\train\\6.jpg"  # replace with your image path
results = model(image_path)  # Detect fields using YOLO

# Load the original image
image = cv2.imread(image_path)

# Dictionary to store extracted fields
extracted_data = {}

# Iterate through detections
for result in results[0].boxes.data.tolist():  # results[0].boxes.data contains bounding box details
    x1, y1, x2, y2, confidence, class_id = map(int, result[:6])
    field_class = model.names[class_id]  # Get class name (e.g., 'Name', 'UID', 'Address')

    # Crop the detected region
    cropped_roi = image[y1:y2, x1:x2]

    # Convert cropped ROI to grayscale for OCR
    gray_roi = cv2.cvtColor(cropped_roi, cv2.COLOR_BGR2GRAY)

    # Use EasyOCR to extract text
    text = reader.readtext(gray_roi, detail=0)  # detail=0 returns only the text

    # Save the text to the extracted_data dictionary
    extracted_data[field_class] = ' '.join(text)  # Combine detected text if multiple lines

# Print the extracted fields
print("Extracted Data:", extracted_data)