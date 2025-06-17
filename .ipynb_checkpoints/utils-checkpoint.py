
import argparse
import os
import cv2
import re
import atexit
import pympi


def get_fps(video):
    capture = cv2.VideoCapture(video)

    if int(cv2.getVersionMajor()) < 3:
        fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
    else:
        fps = capture.get(cv2.CAP_PROP_FPS)
    capture.release()
    return fps


def keypoint_check(arg_list):
    if arg_list == '[]':
        return []
    else:
        return list(map(int, arg_list[1:-1].split(",")))


def init():
    os.chdir(parent(os.path.realpath(__file__)))
    args = parse_args()
    keypoints_left = keypoint_check(args.keypoints_left)
    keypoints_right = keypoint_check(args.keypoints_right)
    keypoints_body = keypoint_check(args.keypoints_body)
    wd = format_path(os.getcwd())
    openpose = posixpath.join(parent(wd, 2), "openpose_gpu", "bin", "OpenPoseDemo.exe")
    fps = get_fps(args.filename)
    return args, openpose, fps, keypoints_left, keypoints_right, keypoints_body

def to_eaf(tiers):
    # takes the individual lists and compiles them into an eaf object
    eaf_out =  pympi.Elan.Eaf()
    for tier_name in tiers:
            eaf_out.add_tier(tier_name)
            
            for annot in tiers[tier_name]:
                eaf_out.add_annotation(tier_name, annot[0], annot[1],annot[2])
                
    return eaf_out



def timestamp_to_ms(timestamp):
    h,m,s = timestamp.split(":")
    ms_time = int((float(s) + (int(m)*60) + ((int(h)*60)*60))*1000)
    
    return ms_time