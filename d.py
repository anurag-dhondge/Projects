from ultralytics import YOLO

def main():
    # Load YOLO model
    model = YOLO("yolov8n.pt")

    # Train the model
    model.train(
        data=r"C:\Users\91989\Desktop\project\dataset\data.yaml",
        epochs=100,
        imgsz=640,
        device=0  # Use GPU 0 (your RTX 3050)
    )

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # Optional for Windows
    main()
