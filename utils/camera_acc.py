import cv2
import sys
import numpy as np
from utils.load_model import modelDetection
from utils.write_db import createLogsDB


class getCameraAcc():
    
    """
    Class descriptions ...
    
    Params:
    ----------
    ....
    
    name: descr ....
    
    """ 

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.s = config.s
    
    
    def get_camera_acc(self):
        
        if len(sys.argv) > 1: 
            self.s = sys.argv[1]

        # creating video capture object by calling VideoCapture class 
        source = cv2.VideoCapture(self.s) 

        win_name = 'Camera'
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

        # creating model object
        model_det = modelDetection(self.config)

        # creating logs object to write data detections in database
        logs_db = createLogsDB(self.config)
        
        while cv2.waitKey(1) != 27: #Escape
            has_frame, frame = source.read()
            if not has_frame:
                break
            frame = cv2.flip(frame, 1) # inverse, around y-axis
            
            # detection people
            preproc_frame, frame_as_tensor = model_det.inference_transforms(frame)
            frame_after_pred, prediction, time_detection, num_peoples = model_det.get_prediction(preproc_frame, 
                                                                                                 frame_as_tensor)
            if time_detection:
                logs_db.add_db(np.datetime_as_string(time_detection, unit='D'), 
                               np.datetime_as_string(time_detection, unit='s')[11:], 
                               num_peoples)
                        
            cv2.imshow(win_name, np.array(frame_after_pred.convert("RGB")))
            #cv2.waitKey(0) # for debugging step by step
        
        logs_db.close_db()
        source.release()
        cv2.destroyWindow(win_name)