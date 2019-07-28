import numpy as np
import cv2
import os 
import shutil


THRESHOLD_LINE = 12

def convertToRectangle(box):
    g1,g2,g3,g4 = box[0], box[1], box[2], box[3]
    x_min = min(g1[0],g4[0])
    y_min = min(g1[1],g4[1])
    x_max = max(g2[0],g3[0])
    y_max = max(g2[1],g3[1])

    g1 = [x_min,y_min]
    g2 = [x_max,y_min]
    g3 = [x_max,y_max]
    g4 = [x_min,y_max]    
    return g1,g2,g3,g4       

def detectLine(boxes, threshold=THRESHOLD_LINE):
    line_dict = dict()
    line_ind = 1
    items = [boxes[0]]
    for i in range(len(boxes)): # range = 0->len()-1
        # Last box
        if i == len(boxes)-1:
            items = sort_box(items)
            line_dict[line_ind] = items
            break

        y_max_curr = boxes[i][3][1]
        y_max_next = boxes[i+1][3][1]
        if  y_max_next - y_max_curr <= threshold:
            items.append(boxes[i+1])

        else:
            # sort box
            items = sort_box(items)

            line_dict[line_ind] = items
            line_ind += 1
            items = [boxes[i+1]]

    print('Number lines detected: {} \n'.format(len(line_dict)))

    return line_dict


def sort_box(boxes):
    for i in range(len(boxes)):
        for j in range(len(boxes)-1):
            if boxes[j][0][0] > boxes[j+1][0][0]:
                temp = boxes[j]
                boxes[j] = boxes[j+1]
                boxes[j+1] = temp 

    return boxes


def cropLine(img_file, img,line_dict, num_line = 1,dirname='./result_line/',):
    img = np.array(img)

    # make result file list
    filename, file_ext = os.path.splitext(os.path.basename(img_file))

    boxes = line_dict[num_line]
    for ind,box in enumerate(boxes):
        x1,y1,x2,y2 = int(box[0][0]),int(box[0][1]),int(box[2][0]),int(box[2][1])
        crop = img[y1:y2,x1:x2]
        res_img_file = dirname + "res_" + filename+'_' +str(ind) + '.jpg'
        # save image
        cv2.imwrite(res_img_file, crop)
