import numpy as np
import math
import PIL 
from PIL import Image

def findAngle(g1,g2):
    '''
    - angle = atan2(det,dot)
    - Return degree
    '''
    v0 = np.array([g2[0]-0, 0])
    v1 = np.array([g2[0]-g1[0], g2[1]-g1[1]])

    angle = np.degrees(np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1)))
    print('Angle = {:.3f} degree'.format(angle))
    return angle

def cal_corner(image,box):
    top, left, bottom, right = box
    padding = 0
    # For larger box 
    top = max(0, np.floor(top - padding).astype('int32'))
    left = max(0, np.floor(left - padding).astype('int32'))
    bottom = min(image.size[1], np.floor(bottom + padding).astype('int32'))
    right = min(image.size[0], np.floor(right + padding).astype('int32'))

    x_center = (left+right)/2
    y_center = (top+bottom)/2
    corner = [x_center, y_center]
    return corner 

def rotate_and_crop(image,corners):
        padding = 5
        if corners[0] != False and corners[2] != False:
            
            angle = 0
            if corners[1] != False:
                angle = findAngle(corners[0], corners[1])
            elif corners[3] != False:
                angle = findAngle(corners[3], corners[2])
            else:
                return image
            corners = rotate_point(image,corners,angle)

            left = corners[0][0]   #x_min
            top = corners[0][1]    #y_min 
            right = corners[2][0]
            bottom = corners[2][1]
            image_rotate = image.rotate(angle,resample = PIL.Image.BICUBIC)  # xoay nguoc chieu kim dong ho
            image_crop = image_rotate.crop((max(0, left-padding),max(0,top-padding),min(image.size[0],right+padding),min(image.size[1],bottom+padding)))


        elif corners[1] != False and corners[3] != False:
            
            angle = 0
            if corners[0] != False:
                angle = findAngle(corners[0], corners[1])
            elif corners[2] != False:
                angle = findAngle(corners[3], corners[2])
            else:
                return image

            corners = rotate_point(image, corners, angle)

            right = corners[1][0]
            top = corners[1][1]
            left = corners[3][0]
            bottom = corners[3][1]
            image_rotate = image.rotate(angle,resample = PIL.Image.BICUBIC)
            image_crop = image_rotate.crop((max(0, left-padding),max(0,top-padding),min(image.size[0],right+padding),min(image.size[1],bottom+padding)))
        else:
            image_crop = image    

        return image_crop


def rotate_point(image, corners, angle):
    '''
    - Rotation corners around center image
    - angle : degreee
    '''
    # Conver to radian 
    angle = math.radians(angle)
    new_corners = []
    w, h = image.size[0], image.size[1]
    center = [w/2,h/2]

    for corner in corners:
        if corner == False:
            new_corners.append(False)
            continue
        # -angle because y-axis downward 
        new_corner = rotate(center, corner, -angle)
        new_corners.append(new_corner)

    return new_corners


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    - For usual axis: x left-right, y bottom-up 
    """
    ox, oy = origin[0],origin[1]
    px, py = point[0],point[1]

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return [qx, qy]


def add_padding_image(img, padding=50):
    w, h = img.size
    w_new, h_new = w + padding*2, h + padding * 2
    new_img = Image.new('RGB', (w_new, h_new), (255,255,255))
    new_img.paste(img, (padding, padding))

    return new_img


