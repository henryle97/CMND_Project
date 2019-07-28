import test 
from craft import CRAFT
import torch 
from PIL import Image
from YoloV3.yolo import YOLO 
import numpy as np 
import cmnd_utils
import shutil
import os 
import file_utils

TRAINED_MODEL = 'craft_mlt_25k.pth'
TEXT_THRESHOLD = 0.9
LOW_TEXT = 0.3
LINK_THRESHOLD = 0.5
CUDA = False 
POLY = False 
RESULT_DETECT_CMND = './result_detect/'
RESUTL_DETECT_TEXT ='./result/'
RESULT_LINE_DIR = './result_line/'
reset_line_dir = True
reset_text_dir = True
reset_detected_cmnd = True
def reset_result():
    if reset_line_dir:
        shutil.rmtree(RESULT_LINE_DIR)
        os.mkdir(RESULT_LINE_DIR)
    if reset_text_dir:
        shutil.rmtree(RESUTL_DETECT_TEXT)
        os.mkdir(RESUTL_DETECT_TEXT)
    if reset_detected_cmnd:
        shutil.rmtree(RESULT_DETECT_CMND)
        os.mkdir(RESULT_DETECT_CMND)

if __name__ == '__main__':
    # No CUDA 
    net = CRAFT()
    net.load_state_dict(test.copyStateDict(torch.load(TRAINED_MODEL, map_location='cpu')))
    # net.eval()
    reset_result()
    # Load image 
    img_path = input('Input image path:')
    try:
        image = Image.open(img_path)
        image = image.convert('RGB')
    
    except:
        print('Open Error! Try again!')
    else:
        # Pre-processing image 

        yolo = YOLO()
        detect_image = yolo.detect_image(image)
        detect_image = np.asarray(detect_image) 
        # Detect text cmnd 
        bboxes, polys, lines = test.test_net(net, detect_image,TEXT_THRESHOLD, LINK_THRESHOLD,LOW_TEXT,CUDA,POLY)
        file_utils.saveResult(img_path, detect_image[:,:,::-1], polys, dirname=RESUTL_DETECT_TEXT)
        cmnd_utils.cropLine(img_path,  detect_image[:,:,::-1],lines, num_line=5, dirname=RESULT_LINE_DIR)



