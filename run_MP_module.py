# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:17:41 2023

@author: jptru

REQUIRES 3 arguments:
    filename  -- the name of the video to be processed
    filepath  -- the path to this video
    outpath   -- the general output directory for processed data

"""
import cv2
import mediapipe
import csv
import os


drawingModule = mediapipe.solutions.drawing_utils #from mediapipe initialize a module that we will use
holModule = mediapipe.solutions.holistic

#take some google classification object and convert it into a string
def makegoginto_str(gogobj):
    gogobj = str(gogobj).strip("[]")
    gogobj = gogobj.split("\n")
    return(gogobj[:-1]) #ignore last element as this has nothing

#landmarks 33x
markers = ['NOSE', 'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_OUTER', 'RIGHT_EYE', 'RIGHT_EYE_OUTER',
          'LEFT_EAR', 'RIGHT_EAR', 'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 
          'RIGHT_ELBOW',
          'LEFT_WRIST', 'RIGHT_WRIST', 
          'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX',
          'LEFT_THUMB', 'RIGHT_THUMB', 
          'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE', 'RIGHT_ANKLE',
          'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']

markers_hand = ["WRIST",
                "THUMB_CMC","THUMB_MCP","THUMB_IP","THUMB_TIP",
                "INDEX_FINGER_MCP","INDEX_FINGER_PIP", "INDEX_FINGER_DIP","INDEX_FINGER_TIP",
                "MIDDLE_FINGER_MCP","MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP","MIDDLE_FINGER_TIP",
                "RING_FINGER_MCP","RING_FINGER_PIP", "RING_FINGER_DIP","RING_FINGER_TIP",
                "PINKY_MCP","PINKY_PIP", "PINKY_DIP","PINKY_TIP"
                ]
    
    
#check if there are numbers in a string
def num_there(s):
    return any(i.isdigit() for i in s)

#make the stringifyd position traces into clean values
def listpostions(newsamplemarks):
    tracking_p = []
    for value in newsamplemarks:
        if num_there(value):
            stripped = value.split(':', 1)[1]
            stripped = stripped.strip() #remove spaces in the string if present
            tracking_p.append(stripped) #add to this list  
    return(tracking_p)


#loop through all the video files and extract pose information
def process_video(filename, filepath, outpath):
    print("Filename = " + filename)
    print("outpath = " + outpath)
    #outpath = outpath + filename.split(".")[0] + "/"
    if not os.path.isdir(outpath):
        os.mkdir(outpath)

    if not filepath.endswith("/"):
        filepath = filepath + "/"
    
    
    if not os.path.isfile(outpath + filename[:-4]+'.csv'):
        #capture the video, and check video settings
        capture = cv2.VideoCapture(filepath+filename)
        frameWidth = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        frameHeight = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = capture.get(cv2.CAP_PROP_FPS)   #fps = frames per second
        print(frameWidth, frameHeight, fps)
        #pose tracking with keypoints save!
        
        #make an 'empty' video file where we project the tracking on
        samplerate = fps #make the same as current video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') #(*'XVID')
        out = cv2.VideoWriter(outpath + filename[:-4]+'.mp4', fourcc, fps = samplerate, frameSize = (int(frameWidth), int(frameHeight)))
    
        #make a variable list with x, y, z, info where data is appended to
            #the markers are initialized above
        markerxyz = []
        for mark in markers:
            for pos in ['X', 'Y', 'Z', 'visibility']:
                nm = pos + "_" + mark
                markerxyz.append(nm)
        addvariable = ['time']
        addvariable.extend(markerxyz)
        
        markerxyz_left_hand = []
        markerxyz_right_hand = []
        for mark in markers_hand:
            for pos in ['X', 'Y', 'Z', 'visibility']:
                nm_L = pos + "_LEFT_" + mark
                nm_R = pos + "_RIGHT_" + mark
                markerxyz_left_hand.append(nm_L)
                markerxyz_right_hand.append(nm_R)
        addvariable.extend(markerxyz_left_hand)
        addvariable.extend(markerxyz_right_hand)
                
        time = 0 #initalize a time variable that starts at 0
        timeseries = [addvariable] #add the first row of column names to your timeseres data object (X_NOSE, .. etc.)
        #MAIN ROUTINE
            #check the settings of your posemodel if you want to finetune (https://google.github.io/mediapipe/solutions/pose.html)
        with holModule.Holistic(min_detection_confidence=0.5, model_complexity = 2, min_tracking_confidence=0.75, smooth_landmarks = True) as holistic:
             while (True):
                ret, frame = capture.read() #read frames
                if ret == True:
                    results = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) #apply the mediapipe pose tracking ont the frame
                    
                    fuldataslice = [str(time)]#this is the first info in the time series slice (time)
                    
                    if results.pose_landmarks != None: #get the ddata from the results if there is info
                        newsamplelmarks = makegoginto_str(results.pose_landmarks)
                        newsamplelmarks = listpostions(newsamplelmarks)
                        fuldataslice.extend(newsamplelmarks) #add positions to this slice
                        #timeseries.append(fuldataslice) #append slice to the timeries data object            
                        drawingModule.draw_landmarks(frame, results.pose_landmarks, holModule.POSE_CONNECTIONS) #draw skeleton
                        #for point in handsModule.HandLandmark: #you can uncomments this if you want to draw points instead of skeleton
                            #normalizedLandmark = results.pose_landmarks.landmark[point]
                            #pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, frameWidth, frameHeight)
                            #cv2.circle(frame, pixelCoordinatesLandmark, 5, (0, 255, 0), -1)

                    else: 
                        fuldataslice.extend([0]*len(markerxyz))
                        #timeseries.append(fuldataslice)
                        
                    if results.left_hand_landmarks != None: 
                        newsamplelmarks = makegoginto_str(results.left_hand_landmarks)
                        newsamplelmarks = listpostions(newsamplelmarks)
                        fuldataslice.extend(newsamplelmarks) #add positions to this slice
                        #timeseries.append(fuldataslice) #append slice to the timeries data object            
                        drawingModule.draw_landmarks(frame, results.left_hand_landmarks)
                    else: 
                        fuldataslice.extend([0]*len(markerxyz_left_hand))
                        #timeseries.append(fuldataslice) 
                        
                    if results.right_hand_landmarks != None: 
                        newsamplelmarks = makegoginto_str(results.right_hand_landmarks)
                        newsamplelmarks = listpostions(newsamplelmarks)
                        fuldataslice.extend(newsamplelmarks) #add positions to this slice
                        #timeseries.append(fuldataslice) #append slice to the timeries data object            
                        drawingModule.draw_landmarks(frame, results.left_hand_landmarks)
                    else: 
                        fuldataslice.extend([0]*len(markerxyz_right_hand))
                        #timeseries.append(fuldataslice) 
                    
                    timeseries.append(fuldataslice) #append slice to the timeries data object       
                    
                    cv2.imshow('MediaPipe Pose', frame) #show the current frame with skeleton tracking
                    out.write(frame)  ######write the frame to your video object######################comment this if you dont want to make a video
                    time = time+(1000/samplerate) #routine is done, next frame will be 1000 milliseconds/samplerate later in time
                    if cv2.waitKey(1) == 27: #allow the use of ESCAPE to break the loop
                        break
                if ret == False: #if there are no more frames, break the loop
                    break
        #once done de-initialize
        out.release()
        capture.release()
        cv2.destroyAllWindows()
    
        ####################################################### data to be written row-wise in csv fil
        # opening the csv file in 'w+' mode
        file = open(outpath + filename[:-4]+'.csv', 'w+', newline ='')
        #write it
        with file:    
            write = csv.writer(file)
            write.writerows(timeseries)
        file.close()


#if __name__ == "__main__":
#    process_video(sys.argv[1], sys.argv[2], sys.argv[3])