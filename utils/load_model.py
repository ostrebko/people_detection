import cv2
import torch

from torchvision.models.detection import ssdlite320_mobilenet_v3_large as model_4_detection
from torchvision.models.detection import SSDLite320_MobileNet_V3_Large_Weights as weights_4_detection
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image



class ModelDetection():
    def __init__(self ):# config: dict
        super().__init__()
        #self.config = config
        self.weights = weights_4_detection.DEFAULT
        self.model = model_4_detection(weights=self.weights,
                                       score_thresh=0.5).eval()

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
            #print(prediction)

            #labels = [self.weights.meta["categories"][i] for i in prediction["labels"]]
            labels = [self.weights.meta["categories"][i] for i in prediction["labels"]]
            #print(labels)

            box = draw_bounding_boxes(initial_img, 
                                  boxes=prediction["boxes"],
                                  labels=labels,
                                  colors="red",
                                  width=4, 
                                  #font_size=30
                                  )
        
            im = to_pil_image(box.detach())
        # im.show()

        return im, prediction
    