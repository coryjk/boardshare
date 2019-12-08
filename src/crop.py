import cv2
import numpy as np

def bound_by_symbol(img, box_info, symbol='#'):
    # parse by new line, isolate symbol of interest
    parsed_info = box_info.split('\n')
    interest_points = [info for info in parsed_info if info[0] == symbol]
    # reality check
    assert len(interest_points) == 4, "Error: no bounding box detected"
    # determine corners from interest points
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
    
    a = (x1, y1, x2, y2), b = (x3, y3, x4, y4)
        --> p1 = (x2, y4)
    c = (x1, y1, x2, y2), d = (x3, y3, x4, y4)
        --> p4 = (x1, y1)

    a: min(y1), b: min(x1), c: max(x1), d: max(y1)
    """
    p_init = interest_points[0].split(' ')
    p_init = p_init[1:len(p_init)-1]
    a, b, c, d = p_init, p_init, p_init, p_init
    # point: {x1, y1, x2, y2}
    for point in interest_points:
        p = point.split(' ')
        p = p[1:len(p)-1]
        # a
        if p[1] < a[1]:
            a = p
        # b
        if p[0] < b[0]:
            b = p
        # c
        if p[0] > c[0]:
            c = p
        # d
        if p[1] > d[1]:
            d = p
    print(a, b, c, d)
    # TODO later...
    return None