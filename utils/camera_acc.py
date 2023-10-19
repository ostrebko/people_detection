# based from opencv free bootcamp

import cv2
import sys 


def get_camera_acc():
    s = 0 #default camera defice index = 0

    if len(sys.argv) > 1: 
        s = sys.argv[1]

    # creating video capture object by calling VideoCapture class 
    source = cv2.VideoCapture(s) 

    win_name = 'Camera'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

    while cv2.waitKey(1) != 27: #Escape
        has_frame, frame = source.read()
        if not has_frame:
            break
        frame = cv2.flip(frame, 1) # inverse, around y-axis
        
        frame_height = frame.shape[0]
        frame_widht = frame.shape[1]

        cv2.imshow(win_name, frame)

    source.release()
    cv2.destroyWindow(win_name)