import cv2
import torch

from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2 as model_4_detection
from torchvision.models.detection import FasterRCNN_ResNet50_FPN_V2_Weights as weights_4_detection
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image



class ModelDetection():
    def __init__(self ):# config: dict
        super().__init__()
        #self.config = config
        self.weights = weights_4_detection.DEFAULT
        self.model = model_4_detection(weights=self.weights, 
                                       box_score_thresh=0.9).eval()

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
        
        # Use the model and visualize the prediction
        prediction = self.model(preproc_img)[0]

        labels = [self.weights.meta["categories"][i] for i in prediction["labels"]]

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


# model_det = ModelDetection()
# # model = model_det.model
# # weights = model_det.weights

# initial_img = cv2.imread('./utils/temp_photo.jpg', cv2.IMREAD_COLOR)

# preproc_img, img_as_tensor = model_det.inference_transforms(initial_img)
# im, prediction = model_det.get_prediction(preproc_img, img_as_tensor)

# win_name = 'Camera'
# cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

# cv2.imshow(win_name, initial_img)
# cv2.waitKey(0)
# cv2.destroyWindow(win_name)