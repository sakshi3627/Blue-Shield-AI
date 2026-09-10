from ultralytics import YOLO

def run_satellite_vessel_detection(image_path):
    # Loads pretrained YOLOv8 model
    model = YOLO("yolov8n.pt") 
    results = model(image_path)
    
    detections = []
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            coords = box.xyxy[0].tolist()
            
            if cls_id == 8 or cls_id == 0:  # Boat or Person/Object
                detections.append({
                    "bounding_box": coords,
                    "confidence": confidence
                })
    return detections

if __name__ == "__main__":
    print("Satellite detection module ready.")
    
