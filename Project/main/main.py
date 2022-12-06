"""
Author: Venkatarao Rebba <rebba498@gmail.com>

It is the main script to run the entire project.

"""

import face_recognition
import cv2
import numpy as np
from MongoDbHandler import MongoDBHandler
from CloudFunctionHandler import CloundFunctionHandler
from TempStorage import TempStorage
import time

mongoDbHandler = MongoDBHandler()
cloudHander = CloundFunctionHandler("credentials.json")
tempStorage = TempStorage()

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
person_counter = 1
process_counter = 0

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Get the registered uses data from MongoDB
known_face_names, known_face_encodings = mongoDbHandler.get_records()

while True:
    ret, frame = video_capture.read()
    
    notFound = False
    # Only process alternative frames
    if process_counter%2 == 0:

        st = time.time()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        notFound = False
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if matches:
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

            if matches and matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            else:
                temp_face_names, temp_face_encodings = tempStorage.getFaceNamesAndEmbeddings()
                matches = face_recognition.compare_faces(temp_face_encodings, face_encoding)

                if matches:
                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(temp_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                if matches and matches[best_match_index]:
                    name = temp_face_names[best_match_index]
                    tempStorage.updateExpiryTime(name, time.time())

                else:
                    print("New Person! Adding him/her in the DB")
                    person_name = f"Person {person_counter}"
                    tempStorage.addNewFace(person_name, face_encoding, time.time())
                
                    person_counter += 1
                    notFound = True
            
            face_names.append(name)
            
        # print(f"Time for Prediction: {time.time() - st}")

    process_counter += 1
    process_this_frame = not process_this_frame

    visual_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # Draw a box around the face
        cv2.rectangle(visual_frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(visual_frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(visual_frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', visual_frame)

    if notFound:
        img_name = f"image_{time.time()}.png"
        cv2.imwrite(img_name,visual_frame)
        # time.sleep(0.5)
        cloudHander.upload_file(img_name)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()