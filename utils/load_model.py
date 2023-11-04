import cv2
import torch
import numpy as np

from torchvision.models.detection import ssdlite320_mobilenet_v3_large as model_4_detection
from torchvision.models.detection import SSDLite320_MobileNet_V3_Large_Weights as weights_4_detection
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image



class modelDetection():
    
    """
    Class descriptions ...
    
    Params:
    ----------
    ....
    
    name: descr ....
    
    """ 
    
    def __init__(self, config:dict):# config: dict
        super().__init__()
        self.config = config
        self.weights = weights_4_detection.DEFAULT
        self.model = model_4_detection(weights=self.weights,
                                       score_thresh=self.config.score_detect_thresh).eval()


    def inference_transforms(self, image):
        
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Transforms: 1. h-w-c to c-h-w 2. to tensor
        img_as_tensor = torch.from_numpy(image.transpose((2, 0, 1))) 
        
        # Initializing the inference transforms
        preprocess = self.weights.transforms()
        
        # Applying inference preprocessing transforms
        preproc_img = [preprocess(img_as_tensor)]

        return preproc_img, img_as_tensor
    
    
    def get_prediction(self, preproc_img, initial_img):
        
        with torch.no_grad():

            # Use the model and visualize the prediction
            prediction = self.model(preproc_img)[0]
            #print(prediction) # for debugging
            
            # use all labels
            #labels = [self.weights.meta["categories"][i] for i in prediction["labels"]]
            #boxes = prediction["boxes"]

            #choose only 1 label
            mask_person = prediction['labels'] == self.config.label_num_category #1
            labels = torch.sum(
                mask_person)*[self.weights.meta["categories"][self.config.label_num_category]] #['person']
            boxes = prediction["boxes"][mask_person]
            num_peoples = len(boxes)
            #print(num_peoples) # for debugging
            #print(labels) # for debugging
            
            if labels:
                box = draw_bounding_boxes(initial_img, 
                                          boxes=boxes,
                                          labels=labels,
                                          colors=self.config.bbox_color,
                                          width=self.config.bbox_width, 
                                          #font_size=30
                                         )
                time_detection = np.datetime64('now') + np.timedelta64(3, 'h')
                im = to_pil_image(box.detach())
            else:
                im = to_pil_image(initial_img)
                time_detection = None
        
        return im, prediction, time_detection, num_peoples
    