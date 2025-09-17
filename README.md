### **License Plate Recognition (LPR) with YOLOv8 & EasyOCR**

This project demonstrates an end-to-end License Plate Recognition (LPR) system using Ultralytics YOLOv8 for object detection and EasyOCR for optical character recognition.

-----

Features

YOLOv8 for license plate detection

EasyOCR for reading text from plates

Cleans and formats detected plate text

Displays detection confidence score

Saves and displays annotated results

-----

### ⚙️ **Usage**

#### **1. Run Detection & OCR**

To run the inference on an image and perform OCR, follow these steps:

1.  Clone the repository and install the required dependencies:
    ```bash
    git clone https://github.com/anurag-dhondge/Python_Project
    pip install -r requirements.txt
    ```
2.  Execute the script with your model weights and an image:
    ```bash
    python main.py --weights yolov8n.pt --source sample_3.png
    ```

The output image with the detected plate bounding box and confidence score will be saved. The detected text will be printed to the console.

#### **2. Train YOLOv8 Model**

To train a custom YOLOv8 model for license plate detection, prepare your dataset and configuration. A GPU is highly recommended for training. The model was trained using an **NVIDIA RTX 3050**.

-----

### 🗂 **Dataset**

The dataset is provided by [Roboflow].

  - **Total Train Images:** **7057**
  - **Total Test Images:** **1020**
  - **Total Valid Images:** **2048**
  - **Format:** YOLOv8 Oriented Object Detection

-----

### 🎯 **Use Cases**

  - **Law Enforcement & Security:** Detect and record license plates for traffic violations or stolen vehicles.
  - **Parking Management:** Automate entry/exit records and parking operations.
  - **Toll Collection:** Automatic identification of vehicles at toll booths.
  - **Access Control:** Secure entry for gated communities, offices, and private properties.
  - **Traffic Monitoring & Statistics:** Analyze traffic patterns and monitor congestion.

-----

### 🎥 **Demo Video**

\<a href="[https://www.linkedin.com/posts/anuragd2004\_machinelearning-computervision-deeplearning-activity-7351669977327763456-hXYg?utm\_source=share\&utm\_medium=member\_desktop\&rcm=ACoAAEAEw2ABWJvpuQzlrapE2CrHdEADk1FSrSI](https://www.linkedin.com/posts/anuragd2004_machinelearning-computervision-deeplearning-activity-7351669977327763456-hXYg?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEAEw2ABWJvpuQzlrapE2CrHdEADk1FSrSI)" target="\_blank"\>
\</a\>

-----

### 📌 **Sample Output**

**Detected Plate: `MH 19 EQ 0001`**

The output shows the detected number plate with its confidence score.

![output_result_with_confidence](https://github.com/user-attachments/assets/0cf48d24-2820-49d6-ab50-192e177911d5)

-----

### 📝 **References**

  - [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
  - [EasyOCR](https://github.com/JaidedAI/EasyOCR)
  - [Roboflow Dataset](https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e)
