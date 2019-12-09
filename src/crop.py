import cv2
import numpy as np

# RGB --> BGR format for opencv2
# https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
def pil_to_cv2(img): 
    cv2_img = np.array(img.convert('RGB'))
    return cv2_img[:,:,::-1].copy()

# format corner points:
#   "S x1 y1 x2 y2" --> [x1, y1, x2, y2]
def format_corners(point):
    print(point)
    p = point.split(' ')
    p = p[1:len(p)-1]
    p = p if type(p[0]) is int else [int(p_i) for p_i in p]
    return p

# draw rectangles on all target symbols
def draw_rectangles(img, points, symbol=None, formatted=False):
    accum_img = pil_to_cv2(img) if type(img) is not np.ndarray else img
    # assume format for points[i]: (x1, y1, x2, y2)
    for p in points:
        # draw rectangles for matched symbols
        if not formatted:
            if p[0] == symbol or symbol is None:
                x1, y1, x2, y2 = format_corners(p)
                y1 = accum_img.shape[0] - y1
                y2 = accum_img.shape[0] - y2
                accum_img = cv2.rectangle(accum_img, (x1, y1), (x2, y2), (255,0,0), 1)
        # in the case points are already formatted
        else:
            x1, y1, x2, y2 = p
            y1 = accum_img.shape[0] - y1
            y2 = accum_img.shape[0] - y2
            accum_image = cv2.rectangle(accum_img, (x1, y1), (x2, y2), (255,0,0), 1)
    return accum_img

# crop images using 4 bounding symbols
"""
    find P = {p1, p2, p3, p4}:
            * only need p1, p4...
        1               2
          p --- a --- p
          |           |
          b   cjk2bg  c
          |           |
          p --- d --- p
        3               4
    
    a = (x1, y1, w1, h1), b = (x2, y2, w2, h2)
        --> p1 = (x2 + w2, y1 + h1)
    c = (x3, y3, w3, h3), d = (x4, y4, w4, h4)
        --> p4 = (x3, y4)

    a: min(y), b: min(x), c: max(x), d: max(y)
"""
def bound_by_symbol(img, box_info, symbol='#', show_boxes=False):
    # parse by new line, isolate symbol of interest
    parsed_info = box_info.split('\n')
    interest_points = [info for info in parsed_info if info[0] == symbol]
    # reality check
    try:
        assert len(interest_points) >= 4
    except AssertionError:
        # draws boxes on error
        print("Error: no bounding box detected--not enough interest points found")
        return draw_rectangles(img, interest_points, symbol=symbol)
    # determine corners from interest points
    p_init = format_corners(interest_points[0])
    a, b, c, d = p_init, p_init, p_init, p_init
    # point: {x1, y1, x2, y2}
    for point in interest_points:
        p = format_corners(point)
        # find symbol points
        a = p if p[1] < a[1] else a
        b = p if p[0] < b[0] else b
        c = p if p[0] > c[0] else c
        d = p if p[1] > d[1] else d
    # ensure valid points
    assert len(a) == 4 and len(b) == 4 and len(c) == 4 and len(d) == 4, \
           "Key point(s) a,b,c,d have wrong sizes: {0},{1},{2},{3}".format(len(a),len(b),len(c),len(d))
    # convert to cv2 image (BGR, Ptr<cv::UMat>)
    result = pil_to_cv2(img)
    # convert to corners
    p1 = (b[2], result.shape[0]-a[3])
    p4 = (c[0], result.shape[0]-d[1])
    # crop rectangular section
    result = result[p4[1]:p1[1],p1[0]:p4[0]]
    # optional dispay of selected rectangles
    if show_boxes:
        with_rectangles = draw_rectangles(img, [a, b, c, d],
                                          symbol=symbol, formatted=True)
        cv2.imshow("Bounding Boxes", with_rectangles)                                        
    return result

# uses criteria of UVA computing id format to aid detection
# --> ([a-z]{2} | [a-z]{3})[1-9]{1}[a-z]{2}
# in english: 2 or 3 letters followed by 1 digit, followed by 2 more letters
"""
    find all-encompassing box given set of boxes
        along roughly the same horizontal axis:
        
                o--o     o---------o-o--o
    o---o o---o |  |     |---o o---o |  |
    |   | |   | |  | --> |   | |   | |  |
    o---o |   | o--o     |---o |   | o--|
          o---o          o-----o---o----o
"""
def detect_computing_ids(img, box_info):
    parsed_info = box_info.split('\n')
    info = []
    for p in parsed_info:
        info.append(p)
    accum = draw_rectangles(img,info)
    cv2.imshow("test",accum)
    print(parsed_info)
    # case 1: id = [a-z]{2}[1-9]{1}[a-z]{2}, |id| = 5

    # case 2: id = [a-z]{3}[1-9]{1}[a-z]{2}, |id| = 6