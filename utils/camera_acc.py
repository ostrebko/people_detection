import cv2
import sys
import numpy as np
from utils.load_model import ModelDetection


class getCameraAcc():
    
    """
    Function descriptions ...
    
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

        model_det = ModelDetection(self.config)
        #model = model_det.model
        #weights = model_det.weights
        
        while cv2.waitKey(1) != 27: #Escape
            has_frame, frame = source.read()
            if not has_frame:
                break
            frame = cv2.flip(frame, 1) # inverse, around y-axis
            
            # detection people
            preproc_frame, frame_as_tensor = model_det.inference_transforms(frame)
            frame_with_bbox, prediction = model_det.get_prediction(preproc_frame, 
                                                                   frame_as_tensor)
            
            # some func to do after detection


            cv2.imshow(win_name, np.array(frame_with_bbox.convert("RGB")))
            #cv2.waitKey(0) # for debugging step by step
            
        source.release()
        cv2.destroyWindow(win_name)