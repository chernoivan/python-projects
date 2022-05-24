import os.path
import pickle
import sys
import face_recognition
from cv2 import cv2 as cv


def train_model_by_img(name):

    if not os.path.exists("dataset"):
        print("[ERROR] there is no directory 'dataset'")
        sys.exit()

    known_encodings = []
    images = os.listdir("dataset")

    for(i, image) in enumerate(images):
        print(f"[+] processing img {i + 1}/{len(images)}")

        face_img = face_recognition.load_image_file(f"dataset/{image}")
        try:
            face_enc = face_recognition.face_encodings(face_img)[0]
        except IndexError:
            print("[ERROR] Face not found")

        if len(known_encodings) == 0:
            known_encodings.append(face_enc)
        else:
            for item in range(0, len(known_encodings)):
                result = face_recognition.compare_faces([face_enc], known_encodings[item])

                if result[0]:
                    known_encodings.append(face_enc)
                    break
                else:
                    break

    print(f"[INFO] Count of processing photos = {len(known_encodings)}")

    data = {
        "name": name,
        "encodings": known_encodings
    }

    with open(f"encodings/{name}_encodings.pickle", "ab") as file:
        pickle.dump(data, file)

    return f"[INFO] File {name}_encodings.pickle successfully created!"


def take_screenshot_from_video():
    cap = cv.VideoCapture("video.MOV")
    count = 0

    while True:
        ret, frame = cap.read()
        fps = round(cap.get(cv.CAP_PROP_FPS))
        multiplier = fps * 1

        if ret:
            frame_id = int(round(cap.get(1)))
            cv.imshow("frame", frame)
            cv.waitKey(20)

            if frame_id % multiplier == 0:
                cv.imwrite(f"dataset_from_video/{count}.jpg", frame)
                count += 1
        else:
            print("[ERROR] Can't get the frame...")
            break

    cap.release()
    cv.destroyAllWindows()


def main():
    print(train_model_by_img("Alla"))
    # take_screenshot_from_video()


if __name__ == '__main__':
    main()
