import os
import pickle
from datetime import datetime
import numpy as np
from cv2 import cv2
import face_recognition
from PIL import Image, ImageDraw


# face detection in the photo
def face_rec(img_path):
    img = face_recognition.load_image_file(img_path)
    img_face_location = face_recognition.face_locations(img)

    print(img_face_location)

    pil_img = Image.fromarray(img)
    draw = ImageDraw.Draw(pil_img)

    for (top, right, bottom, left) in img_face_location:
        draw.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=4)

    del draw
    pil_img.save(f"img/new_gal_{datetime.now()}.jpg")


def extracting_face(img_path):
    count = 0
    faces = face_recognition.load_image_file(img_path)
    faces_locations = face_recognition.face_locations(faces)

    for face_location in faces_locations:
        top, right, bottom, left = face_location

        face_img = faces[top:bottom, left:right]
        pil_img = Image.fromarray(face_img)
        pil_img.save(f"img/{count}_face_img.jpg")
        count += 1

    return f"Found {count} face(s) in this photo"


# face comparison
def compare_faces(img1_path, img2_path):
    img1 = face_recognition.load_image_file(img1_path)
    img1_encodings = face_recognition.face_encodings(img1)[0]

    img2 = face_recognition.load_image_file(img2_path)
    img2_encodings = face_recognition.face_encodings(img2)[0]

    result = face_recognition.compare_faces([img1_encodings], img2_encodings)
    print(result)


# face detection in the video
def detect_person_in_video():
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir("encodings"):
        data = pickle.loads(open(f"encodings/{filename}", "rb").read())
        known_face_encodings.append(data["encodings"][0])
        known_face_names.append(data["name"])

    video = cv2.VideoCapture(0)

    face_locations = []
    face_names = []
    process_this_frame = True

    print("[INFO] Detected is ran")

    while True:
        ret, frame = video.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

        cv2.imshow("*** Detected is running ***", frame)

        k = cv2.waitKey(20)
        if k == ord("q"):
            print("[INFO] Closing the app")
            break

    video.release()
    cv2.destroyAllWindows()


def main():
    # face_rec("img/gal.jpeg")
    # print(extracting_face("img/gal.jpeg"))
    # compare_faces("img/gal.jpeg", "img/gal2.jpeg")
    detect_person_in_video()


if __name__ == '__main__':
    main()
