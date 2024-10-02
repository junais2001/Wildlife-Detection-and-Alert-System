from ultralytics import YOLO
import cv2
import winsound

# Load the YOLO model
model = YOLO(r"C:\Users\Acer\Downloads\Animal_best.pt")

# Function to check for specific animal classes and count how many are detected
def count_animals(class_ids):
    # Classes that trigger the alert
    animal_classes = ['Deer', 'Elephant', 'Tiger']
    detected_animals = 0

    # Count how many of the detected classes are animals
    for class_id in class_ids:
        class_name = model.names[int(class_id)]
        if class_name in animal_classes:
            detected_animals += 1

    return detected_animals

# Function to send alert based on the number of detected animals
def send_alert(animal_count):
    if animal_count > 0:
        print(f"ALERT: {animal_count} dangerous animal(s) detected!")
        winsound.Beep(1000, 500)  # Beep sound for the alert
        if animal_count >= 2:
            # If more than one animal is detected, increase alert intensity
            winsound.Beep(1200, 700)  # Higher pitch for multiple animals
        # if animal_classes =="Deer":
        #     print("the detected animal is Deer")
        # if animal_classes =="Tiger":
        #     print("the detected animal is Deer")
        # if animal_classes =="Elephant":
        #     print("the detected animal is Deer")
        

def main():
    # Replace the 0 with your video file path
    cap = cv2.VideoCapture(r"C:\Users\Acer\Downloads\2835528-hd_1920_1080_25fps.mp4"q)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO detection and tracking
        results = model.track(frame, tracker="bytetrack.yaml")

        # Initialize an empty list to store class ids from the detection results
        class_ids = []

        # Gather class IDs from detection results
        for result in results:
            class_ids.extend(result.boxes.cls)

            # Plot the detection results on the frame
            annotated_frame = result.plot()

        # Count the number of detected animals (Deer, Elephant, Tiger)
        animal_count = count_animals(class_ids)

        # Send alert if any animals are detected
        if animal_count > 0:
            send_alert(animal_count)

        # Display the annotated frame
        cv2.imshow('Frame', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
