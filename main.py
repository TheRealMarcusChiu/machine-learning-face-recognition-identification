import cv2
import os
import numpy as np

people = ["",
          "Matt Damon",
          "Emma Watson"]


# assumption: img contains 0 or 1 face
def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('lbp.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    if len(faces) == 0:
        return None, None

    (x, y, w, h) = faces[0]
    
    return gray[y:y+w, x:x+h], faces[0]


def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    
    faces = []
    labels = []
    
    for dir_name in dirs:
        if not dir_name.startswith("s"):
            continue

        label = int(dir_name.replace("s", ""))
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue
            
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            
            cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
            cv2.waitKey(100)
            
            face, rect = detect_face(image)

            if face is not None:
                faces.append(face)
                labels.append(label)
            
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    return faces, labels


print("Preparing data...")
faces, labels = prepare_training_data("training-data")
print(faces)
print("Data prepared")

print("Total faces: ", len(faces))
print("Total labels: ", len(labels))


# instantiate face-recognizer: LBPH, Eigen, Fisher
face_identifier = cv2.face.LBPHFaceRecognizer_create()
# face_identifier = cv2.face.EigenFaceRecognizer_create()
# face_identifier = cv2.face.FisherFaceRecognizer_create()


# training time
face_identifier.train(faces, np.array(labels))


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)
    

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 4)


def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)

    label, confidence = face_identifier.predict(face)
    label_text = people[label]
    
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    
    return img


print("Predicting images...")

# load test images
test_img1 = cv2.imread("test-data/test1.jpg")
test_img2 = cv2.imread("test-data/test2.jpg")


# perform a prediction
predicted_img1 = predict(test_img1)
predicted_img2 = predict(test_img2)
print("Prediction complete")

# save images
cv2.imwrite('output-data/1.jpg', predicted_img1)
cv2.imwrite('output-data/2.jpg', predicted_img2)

# display images
cv2.imshow(people[1], cv2.resize(predicted_img1, (400, 500)))
cv2.imshow(people[2], cv2.resize(predicted_img2, (400, 500)))
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()





