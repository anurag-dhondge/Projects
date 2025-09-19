#Import Required Libraries
from ultralytics import YOLO
import cv2
import easyocr
import matplotlib.pyplot as plt
import re


# Load YOLOv8 model (Update the path if needed)
model = YOLO(r"C:\Users\91989\runs\detect\train12\weights\best.pt")


# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=True)


# Load the input image
image_path = r"C:\Users\91989\Desktop\project\sample_images\sample_3.png"
image = cv2.imread(image_path)


# Run detection
results = model(image)


# Function to clean OCR result
def clean_plate_text(text):
    # Remove any unwanted characters like "IND", quotes, spaces, etc.
    text = re.sub(r'[^A-Za-z0-9]+', '', text)  # Remove non-alphanumeric characters
    text = text.replace("IND", "")  # Remove "IND"
    return text


# Process detections
for result in results:
    for box in result.boxes.xyxy: # using .xyxy (top-left to bottom-right format).
        x1, y1, x2, y2 = map(int, box) #Get coordinates of the detected plate and crop that area from the image.
        plate_img = image[y1:y2, x1:x2]
        gray_plate = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY) #Grayscale helps OCR perform better by reducing noise.
        ocr_results = reader.readtext(gray_plate)
        
        
#Extract & Clean OCR Text
        plate_text_fragments = []
        total_confidence = 0
        count = 0
        for detection in ocr_results:
            _, text, conf = detection
            cleaned_text = clean_plate_text(text)
            if conf > 0.4 and cleaned_text:  # Only include if confidence > 0.4 and text is not empty
                plate_text_fragments.append(cleaned_text)
                total_confidence += conf
                count += 1
                
                
        # Combine all fragments into a single text
        full_plate = ''.join(plate_text_fragments)

        if count > 0:
            avg_confidence = total_confidence / count  # Calculate average confidence
        else:
            avg_confidence = 0

        print(f"\n📌 Full Detected Plate: {full_plate} (Confidence: {avg_confidence:.2f})")


        # Draw rectangle and put text with confidence on the image
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        font_scale = 1.5 if avg_confidence < 0.8 else 1.2
        cv2.putText(image, f'{full_plate} ({avg_confidence*100:.1f}%)', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), 2)


# Save and show result
output_path = "output_result_with_confidence.jpg"
cv2.imwrite(output_path, image)
print("\n✅ Saved output image as", output_path)


# Display result
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(rgb_image)
plt.title("Detected Number Plate")
plt.axis('off')
plt.show()