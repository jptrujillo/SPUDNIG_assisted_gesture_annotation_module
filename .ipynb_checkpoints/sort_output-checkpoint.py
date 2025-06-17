# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:11:10 2019

updated 09-03-2023 for SPUDNIG2.1.0
@jptrujillo

@author: jorrip
"""
import posixpath
import json
#import sys
import numpy as np
import pandas as pd
import os
from math import hypot
from scipy import signal
#import pickle

def keypoint_check(arg_list, range_factor):
    if arg_list == '[]':
        return []
    else:
        return [i for i in range(range_factor) if int(i / 3) in arg_list]


def find_first_nonempty_file(root):
    for _, _, files in os.walk(root):
        for file in files:
            with open(posixpath.join(root, file), "r") as read_file:
                data = json.load(read_file)
                if data['people']:
                    return data

def sort_MP(root, keypoints_left, keypoints_right, keypoints_body, video_name):
    left_hand_kp = pd.DataFrame()
    right_hand_kp = pd.DataFrame()
    body_kp = pd.DataFrame()
    
    # for testing
    #with open(root + "keypoints_.pkl", "wb") as f:
    #    pickle.dump([keypoints_left,keypoints_right, keypoints_body], f)
    #with open(outpath +"keypoints_mp.pkl","rb" ) as f:
    #    keypoints_left, keypoints_right, keypoints_body = pickle.load(f)
    
   # keypoints_left = keypoint_check(keypoints_left, 63)
   # keypoints_right = keypoint_check(keypoints_right, 63)
   # keypoints_body = keypoint_check(keypoints_body, 84)
    
    # note that the keypoints are saved as a list of numbers
    # body includes elbow and wrist
    # 9:11: left elbow
    # 12:14: left wrist
    # 18:20: right elbow
    # 21:23: right wrist
    # all others fall under hand
    # main ones:
        # 0:2: palm
        # 12:14 thumb tip
        # 24:26 index tip
        # 60:62 pinky tip
        

        
    hand_dict_L = {4:'X_LEFT_THUMB_CMC',5:'Y_LEFT_THUMB_CMC',6:'Z_LEFT_THUMB_CMC',7:'visibility_LEFT_THUMB_CMC',
                8:'X_LEFT_THUMB_MCP',9:'Y_LEFT_THUMB_MCP',10:'Z_LEFT_THUMB_MCP',11:'visibility_LEFT_THUMB_MCP',
                12:'X_LEFT_THUMB_IP',13:'Y_LEFT_THUMB_IP',14:'Z_LEFT_THUMB_IP',15:'visibility_LEFT_THUMB_IP',
                16:'X_LEFT_THUMB_TIP',17:'Y_LEFT_THUMB_TIP',18:'Z_LEFT_THUMB_TIP',19:'visibility_LEFT_THUMB_TIP',
                20:'X_LEFT_INDEX_FINGER_MCP',21:'Y_LEFT_INDEX_FINGER_MCP',22:'Z_LEFT_INDEX_FINGER_MCP',23:'visibility_LEFT_INDEX_FINGER_MCP',
                24:'X_LEFT_INDEX_FINGER_PIP',25:'Y_LEFT_INDEX_FINGER_PIP',26:'Z_LEFT_INDEX_FINGER_PIP',27:'visibility_LEFT_INDEX_FINGER_PIP',
                28:'X_LEFT_INDEX_FINGER_DIP',29:'Y_LEFT_INDEX_FINGER_DIP',30:'Z_LEFT_INDEX_FINGER_DIP',31:'visibility_LEFT_INDEX_FINGER_DIP',
                32:'X_LEFT_INDEX_FINGER_TIP',33:'Y_LEFT_INDEX_FINGER_TIP',34:'Z_LEFT_INDEX_FINGER_TIP',35:'visibility_LEFT_INDEX_FINGER_TIP',
                36:'X_LEFT_MIDDLE_FINGER_MCP',37:'Y_LEFT_MIDDLE_FINGER_MCP',38:'Z_LEFT_MIDDLE_FINGER_MCP',39:'visibility_LEFT_MIDDLE_FINGER_MCP',
                40:'X_LEFT_MIDDLE_FINGER_PIP',41:'Y_LEFT_MIDDLE_FINGER_PIP',42:'Z_LEFT_MIDDLE_FINGER_PIP',43:'visibility_LEFT_MIDDLE_FINGER_PIP',
                44:'X_LEFT_MIDDLE_FINGER_DIP',45:'Y_LEFT_MIDDLE_FINGER_DIP',46:'Z_LEFT_MIDDLE_FINGER_DIP',47:'visibility_LEFT_MIDDLE_FINGER_DIP',
                48:'X_LEFT_MIDDLE_FINGER_TIP',49:'Y_LEFT_MIDDLE_FINGER_TIP',50:'Z_LEFT_MIDDLE_FINGER_TIP',51:'visibility_LEFT_MIDDLE_FINGER_TIP',
                52:'X_LEFT_RING_FINGER_MCP',53:'Y_LEFT_RING_FINGER_MCP',54:'Z_LEFT_RING_FINGER_MCP',55:'visibility_LEFT_RING_FINGER_MCP',
                56:'X_LEFT_RING_FINGER_PIP',57:'Y_LEFT_RING_FINGER_PIP',58:'Z_LEFT_RING_FINGER_PIP',59:'visibility_LEFT_RING_FINGER_PIP',
                60:'X_LEFT_RING_FINGER_DIP',61:'Y_LEFT_RING_FINGER_DIP',62:'Z_LEFT_RING_FINGER_DIP',63:'visibility_LEFT_RING_FINGER_DIP',
                64:'X_LEFT_RING_FINGER_TIP',65:'Y_LEFT_RING_FINGER_TIP',66:'Z_LEFT_RING_FINGER_TIP',67:'visibility_LEFT_RING_FINGER_TIP',
                68:'X_LEFT_PINKY_MCP',69:'Y_LEFT_PINKY_MCP',70:'Z_LEFT_PINKY_MCP',71:'visibility_LEFT_PINKY_MCP',
                72:'X_LEFT_PINKY_PIP',73:'Y_LEFT_PINKY_PIP',74:'Z_LEFT_PINKY_PIP',75:'visibility_LEFT_PINKY_PIP',
                76:'X_LEFT_PINKY_DIP',77:'Y_LEFT_PINKY_DIP',78:'Z_LEFT_PINKY_DIP',79:'visibility_LEFT_PINKY_DIP',
                80:'X_LEFT_PINKY_TIP',81:'Y_LEFT_PINKY_TIP',82:'Z_LEFT_PINKY_TIP',83:'visibility_LEFT_PINKY_TIP'
                 }
    hand_dict_R = {4:'X_RIGHT_THUMB_CMC',5:'Y_RIGHT_THUMB_CMC',6:'Z_RIGHT_THUMB_CMC',7:'visibility_RIGHT_THUMB_CMC',
                8:'X_RIGHT_THUMB_MCP',9:'Y_RIGHT_THUMB_MCP',10:'Z_RIGHT_THUMB_MCP',11:'visibility_RIGHT_THUMB_MCP',
                12:'X_RIGHT_THUMB_IP',13:'Y_RIGHT_THUMB_IP',14:'Z_RIGHT_THUMB_IP',15:'visibility_RIGHT_THUMB_IP',
                16:'X_RIGHT_THUMB_TIP',17:'Y_RIGHT_THUMB_TIP',18:'Z_RIGHT_THUMB_TIP',19:'visibility_RIGHT_THUMB_TIP',
                20:'X_RIGHT_INDEX_FINGER_MCP',21:'Y_RIGHT_INDEX_FINGER_MCP',22:'Z_RIGHT_INDEX_FINGER_MCP',23:'visibility_RIGHT_INDEX_FINGER_MCP',
                24:'X_RIGHT_INDEX_FINGER_PIP',25:'Y_RIGHT_INDEX_FINGER_PIP',26:'Z_RIGHT_INDEX_FINGER_PIP',27:'visibility_RIGHT_INDEX_FINGER_PIP',
                28:'X_RIGHT_INDEX_FINGER_DIP',29:'Y_RIGHT_INDEX_FINGER_DIP',30:'Z_RIGHT_INDEX_FINGER_DIP',31:'visibility_RIGHT_INDEX_FINGER_DIP',
                32:'X_RIGHT_INDEX_FINGER_TIP',33:'Y_RIGHT_INDEX_FINGER_TIP',34:'Z_RIGHT_INDEX_FINGER_TIP',35:'visibility_RIGHT_INDEX_FINGER_TIP',
                36:'X_RIGHT_MIDDLE_FINGER_MCP',37:'Y_RIGHT_MIDDLE_FINGER_MCP',38:'Z_RIGHT_MIDDLE_FINGER_MCP',39:'visibility_RIGHT_MIDDLE_FINGER_MCP',
                40:'X_RIGHT_MIDDLE_FINGER_PIP',41:'Y_RIGHT_MIDDLE_FINGER_PIP',42:'Z_RIGHT_MIDDLE_FINGER_PIP',43:'visibility_RIGHT_MIDDLE_FINGER_PIP',
                44:'X_RIGHT_MIDDLE_FINGER_DIP',45:'Y_RIGHT_MIDDLE_FINGER_DIP',46:'Z_RIGHT_MIDDLE_FINGER_DIP',47:'visibility_RIGHT_MIDDLE_FINGER_DIP',
                48:'X_RIGHT_MIDDLE_FINGER_TIP',49:'Y_RIGHT_MIDDLE_FINGER_TIP',50:'Z_RIGHT_MIDDLE_FINGER_TIP',51:'visibility_RIGHT_MIDDLE_FINGER_TIP',
                52:'X_RIGHT_RING_FINGER_MCP',53:'Y_RIGHT_RING_FINGER_MCP',54:'Z_RIGHT_RING_FINGER_MCP',55:'visibility_RIGHT_RING_FINGER_MCP',
                56:'X_RIGHT_RING_FINGER_PIP',57:'Y_RIGHT_RING_FINGER_PIP',58:'Z_RIGHT_RING_FINGER_PIP',59:'visibility_RIGHT_RING_FINGER_PIP',
                60:'X_RIGHT_RING_FINGER_DIP',61:'Y_RIGHT_RING_FINGER_DIP',62:'Z_RIGHT_RING_FINGER_DIP',63:'visibility_RIGHT_RING_FINGER_DIP',
                64:'X_RIGHT_RING_FINGER_TIP',65:'Y_RIGHT_RING_FINGER_TIP',66:'Z_RIGHT_RING_FINGER_TIP',67:'visibility_RIGHT_RING_FINGER_TIP',
                68:'X_RIGHT_PINKY_MCP',69:'Y_RIGHT_PINKY_MCP',70:'Z_RIGHT_PINKY_MCP',71:'visibility_RIGHT_PINKY_MCP',
                72:'X_RIGHT_PINKY_PIP',73:'Y_RIGHT_PINKY_PIP',74:'Z_RIGHT_PINKY_PIP',75:'visibility_RIGHT_PINKY_PIP',
                76:'X_RIGHT_PINKY_DIP',77:'Y_RIGHT_PINKY_DIP',78:'Z_RIGHT_PINKY_DIP',79:'visibility_RIGHT_PINKY_DIP',
                80:'X_RIGHT_PINKY_TIP',81:'Y_RIGHT_PINKY_TIP',82:'Z_RIGHT_PINKY_TIP',83:'visibility_RIGHT_PINKY_TIP'
                 }
    # hand_dict_R = {12: "X_RIGHT_THUMB", 13: "Y_RIGHT_THUMB", 14: "visibility_RIGHT_THUMB",
    #              24: "X_RIGHT_INDEX", 25: "Y_RIGHT_INDEX", 26: "visibility_RIGHT_INDEX",
    #              60: "X_RIGHT_PINKY", 61: "Y_RIGHT_PINKY", 62: "visibility_RIGHT_PINKY"}
    body_dict = {9: "X_LEFT_ELBOW", 10: "Y_LEFT_ELBOW",11: "visibility_LEFT_ELBOW",
                 12: "X_LEFT_WRIST", 13: "Y_LEFT_WRIST", 14: "visibility_LEFT_WRIST",
                 18: "X_RIGHT_ELBOW", 19: "Y_RIGHT_ELBOW", 20: "visibility_RIGHT_ELBOW",
                 21: "X_RIGHT_WRIST", 22: "Y_RIGHT_WRIST", 23: "visibility_RIGHT_WRIST",
                 }
        
    mp_keypoints_left = [hand_dict_L[kp] for kp in keypoints_left if kp in hand_dict_L]
    mp_keypoints_right = [hand_dict_R[kp] for kp in keypoints_right if kp in hand_dict_R]
    mp_keypoints_body = [body_dict[kp] for kp in keypoints_body if kp in body_dict]
    # these are needed for all subsequent functions
    mp_keypoints_left_idx = [kp for kp in keypoints_left if kp in hand_dict_L]
    mp_keypoints_right_idx = [kp for kp in keypoints_right if kp in hand_dict_R]
    mp_keypoints_body_idx = [kp for kp in keypoints_body if kp in body_dict]
    
    # for testing
   # with open(root + "keypoints_mp.pkl", "wb") as f:
    #    pickle.dump([mp_keypoints_left_idx,mp_keypoints_right_idx, mp_keypoints_body_idx], f)
    
    
    
    for files in os.listdir(root):
        if files == video_name + ".csv":
           # with open(root + "rootfiles.pkl","wb") as f:
            #    pickle.dump([root, files],f)
            df = pd.read_csv(root + files)
            left_hand_kp = df[[c for c in df.columns if c in mp_keypoints_left]]
            right_hand_kp = df[[c for c in df.columns if c in mp_keypoints_right]]
            body_kp = df[[c for c in df.columns if c in mp_keypoints_body]]
            
    #if left_hand_kp.empty:
    #    left_hand_kp.append(pd.Series([0,0,0]),ignore_index=True)

   # if right_hand_kp.empty:
    #    right_hand_kp.append(pd.Series([0,0,0]),ignore_index=True)
   # if body_kp.empty:    
    #    body_kp.append(pd.Series([0,0,0]),ignore_index=True)         


    left_hand_kp.to_csv(posixpath.join(root, 'hand_left_sample.csv'), encoding='utf-8', index=False, header=None)
    right_hand_kp.to_csv(posixpath.join(root, 'hand_right_sample.csv'), encoding='utf-8', index=False, header=None)
    body_kp.to_csv(posixpath.join(root, 'body_sample.csv'), encoding='utf-8', index=False, header=None)
    
    return mp_keypoints_left_idx, mp_keypoints_right_idx, mp_keypoints_body_idx
    


def create_velocity_file(root, pose_data, keypoint_name):
    # calculate velocity
    vel = []
    timestamps = []
    idx = 0
    for idx1 in range(1,len(pose_data)):
        coords = [pose_data[0][idx1],pose_data[1][idx1]]
        prev_coords = [pose_data[0][idx], pose_data[1][idx]]
        displacement = hypot(float(coords[0]) - float(prev_coords[0]),float(coords[1]) - float(prev_coords[1]))
        vel.append(displacement*25)
        
        # create timestamps
        timestamps.append(frameToTime(idx, 25))
        
        idx += 1
    
    # smooth
    vel_S = signal.savgol_filter(vel, 7,5)
    
    vel_csv = pd.DataFrame(np.column_stack([timestamps,vel_S]),
                                 columns=['time','velocity'])
    
    filename = keypoint_name + '_velocity_track.csv'
    vel_csv.to_csv(posixpath.join(root, filename), encoding='utf-8', index=False, header=None)
    

def frameToTime(i, fps):
    '''Converts the framenumber to hh:mm:ss:ms format'''
    ms_in_h = 3600000
    ms_in_m = 60000
    ms_in_s = 1000

    ms = int(i * (1000 / fps))

    hours = ms // ms_in_h
    ms = ms - (hours * ms_in_h)

    minutes = ms // ms_in_m
    ms = ms - (minutes * ms_in_m)

    s = ms // ms_in_s
    ms = ms - (s * ms_in_s)
    
    return "{0:.0f}:{1:.0f}:{2:.0f}.{3:0>3d}".format(hours, minutes, s, ms)

    