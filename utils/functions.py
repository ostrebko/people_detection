import cv2


def show_image(image):
    
    # show the image
    window_name = 'initial_photo'
    cv2.imshow(window_name, image)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()