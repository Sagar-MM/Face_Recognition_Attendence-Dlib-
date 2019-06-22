import face_recognition
import cv2
import numpy as np
import pandas as pd
import datetime
import time
import csv
import subprocess
from PyQt5 import QtCore
import shutil
#####
#from openpyxl import Workbook
#####

rollNo=[]
known_face_encodings=[]
known_face_names=[]




def copyImage(fileName,userName,userRollNo):
    src=fileName
    studentName=userName
    studentrollNo=userRollNo
    imageName=studentName + "_" + studentrollNo
    dst= "Students/" + imageName + ".jpg"  
    shutil.copyfile(src, dst)
    
    row = [studentrollNo , studentName]
    csv.register_dialect("myDialect",lineterminator = '\n')
    with open('StudentDetails.csv','a+') as csvFile:
        writer = csv.writer(csvFile, dialect="myDialect")
        writer.writerow(row)
    csvFile.close()
    



# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
def openAttendence():
    # subprocess.Popen("StudentDetails.csv",shell=True)    
    subprocess.call("explorer StudentDetails.csv")

def keyPressEvent(self, e):  
    if e.key() == QtCore.Qt.Key_Escape:
        self.close()
    if e.key() == QtCore.Qt.Key_F11:
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
def recognize():
    video_capture = cv2.VideoCapture(0)
    
    df=pd.read_csv("StudentDetails.csv")
    # Load a sample picture and learn how to recognize it.
    for student in df.index:    
        sname= str(df['Name'][student])
        imagerollNo= str(df['rollNo'][student])
        imageName=sname + "_" + imagerollNo
        image=sname+"image"
        known_face_names.append(sname)
        encodingname=sname+"_face_encoding"        
        image= face_recognition.load_image_file("Students\\" + imageName + ".jpg" )
        encodingname = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encodingname)

    

    

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    df=pd.read_csv("StudentDetails.csv")   
    df.set_index('Name',inplace=True)        
    col_names =  ['rollNo','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)
    process_this_frame = True

    

    while True:
        
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1,model='hog')
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.7)
                name = "Unknown"
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    
                    print(name)
                    # if int(name) in range(1,61):
                    #     sheet.cell(row=int(name), column=int(today)).value = "Present"
                    # else:
                    #     pass
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    print(df.loc[name])
                    # aa=df.loc[df['rollNo'] == rollNo]['Name'].values
                    # print(aa)
                    # tt=str(rollNo)+"-"+aa
                    # attendance.loc[len(attendance)] = [rollNo,aa,date,timeStamp]

                face_names.append(name)
            attendance=attendance.drop_duplicates(subset=['rollNo'],keep='first')
            
        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

         # Save Woorksheet as present month
        # book.save(str(month)+'.xlsx')

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # else:
            # ts = time.time()      
            # date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            # timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            # Hour,Minute,Second=timeStamp.split(":")
            # fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
            # attendance.to_csv(fileName,index=False)
            # res=attendance

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
