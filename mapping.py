import numpy as np
import cv2
import math


# Checks if the point lies inside the circle
def obst_circle(point, dim, tol):
    increase = dim + tol
    center = [300, 65]
    coordinate_x = point[0]
    coordinate_y = point[1]
    dist = np.sqrt((coordinate_x - center[0]) ** 2 + (coordinate_y - center[1]) ** 2)
    if dist <= 40 + increase:
        return True
    else:
        return False


# For intersection point of the lines
def intersect_point(c1, c2):
    det = abs(c1[0] - c2[0])

    x_coord, y_coord = None, None
    if det is not 0:
        x_coord = int(round(abs((c1[1] - c2[1])) / det))
        y_coord = int(round(abs(((c1[0] * c2[1]) - (c2[0] * c1[1]))) / det))

    return [x_coord, y_coord]


# Output the new coordinates of the hexagon obstacle
def hexa_points(dim, tol):
    increase = dim + tol
    p1 = [200, 109]
    p2 = [235, 129]
    p3 = [235, 170]
    p4 = [200, 190]
    p5 = [165, 170]
    p6 = [165, 129]

    coff1 = np.array(np.polyfit([p1[0], p2[0]], [p1[1], p2[1]], 1))
    coff2 = np.array(np.polyfit([p2[0], p3[0]], [p2[1], p3[1]], 1))
    coff3 = np.array(np.polyfit([p3[0], p4[0]], [p3[1], p4[1]], 1))
    coff4 = np.array(np.polyfit([p4[0], p5[0]], [p4[1], p5[1]], 1))
    coff5 = np.array(np.polyfit([p5[0], p6[0]], [p5[1], p6[1]], 1))
    coff6 = np.array(np.polyfit([p6[0], p1[0]], [p6[1], p1[1]], 1))

    if increase < 1:
        return p1, p2, p3, p4, p5, p6
    else:
        # change the intercept formed by the lines
        coff1[1] = coff1[1] - (increase / (math.sin(1.57 - math.atan(coff1[0]))))
        coff2[1] = coff2[1] - (increase / (math.sin(1.57 - math.atan(coff2[0]))))
        coff3[1] = coff3[1] - (increase / (math.sin(1.57 - math.atan(coff3[0]))))
        coff4[1] = coff4[1] + (increase / (math.sin(1.57 - math.atan(coff4[0]))))
        coff5[1] = coff5[1] + (increase / (math.sin(1.57 - math.atan(coff5[0]))))
        coff6[1] = coff6[1] + (increase / (math.sin(1.57 - math.atan(coff6[0]))))

        # Keep the slope constant but changing intercept find the intersection point
        p2 = intersect_point(coff1, coff2)
        p3 = intersect_point(coff2, coff3)
        p4 = intersect_point(coff3, coff4)
        p5 = intersect_point(coff4, coff5)
        p6 = intersect_point(coff5, coff6)
        p1 = intersect_point(coff6, coff1)

        return p1, p2, p3, p4, p5, p6


def obst_hexa(pt, points_updated):
    
    contours= [np.array([[203, 106], [238, 126], [238, 170], [203, 193], [162, 170], [162, 129]], dtype=np.int32)] 
    drawing=np.zeros([400,250],np.uint8)
    cv2.drawContours(drawing,contours, -1, (36, 255, 12), 2)
    result1 = cv2.pointPolygonTest(np.array([[203, 106], [238, 126], [238, 170], [203, 193], [162, 170], [162, 129]]), (pt[0],pt[1]), False)
    if(result1)<0:
        return False
    elif(result1>0):
        return True
    else :
        return True


def obst_arrow(pt, points_updated):
    contours= [np.array([[117,36], [30,65], [105,156], [85,70]], dtype=np.int32)] 
    drawing=np.zeros([400,250],np.uint8)
    cv2.drawContours(drawing,contours, -1, (36, 255, 12), 2)
    result1 = cv2.pointPolygonTest(np.array([[117,36], [30,65], [105,156], [85,70]]), (pt[0],pt[1]), False)
    if(result1)<0:
        return False
    elif(result1>0):
        return True
    else :
        return True
    

def obst_flag(point, dim, tol, points_updated):
    if obst_hexa(point, points_updated):
        return True
    elif obst_arrow(point,points_updated):
        return True
    elif obst_circle(point, dim, tol):
        return True
    else:
        return False

# plot the Shapes in the image layout Map. 
def plot_image(object_points, dim, tol):
    increase = dim + tol
    img = 255 * np.zeros((251, 401, 3), np.uint8)

    # Plot the the Hexagon shape
    Hexa_points = np.array([object_points[1], object_points[2], object_points[3], object_points[4], object_points[5]],
                            dtype=np.int32)
    Hexa_map = np.array([[200, 109], [235, 129], [235, 170], [200, 190], [165, 170], [165, 129]],
                           dtype=np.int32)
    
    cv2.fillConvexPoly(img, Hexa_points,(0,127,0))
    cv2.fillConvexPoly(img, Hexa_map, (0,127,0))

    # Plot Arrow 
    arrow_points = np.array([[115,40], [36,65], [105,150], [80,70]],
                            dtype=np.int32)
    arrow_map = np.array([[115,40], [36,65], [105,150], [80,70]],
                           dtype=np.int32)
    cv2.fillConvexPoly(img, arrow_points, (0,127,0))
    cv2.fillConvexPoly(img, arrow_map, (0,127,0))
    
    # Plot the circle
    cv2.circle(img, (300, 65), 40 + increase - 1,(0,127,0), -1)
    cv2.circle(img, (300, 65), 40 - 1, (0,127,0), -1)

    return img
