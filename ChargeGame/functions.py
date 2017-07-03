from math import *
__author__ = 'Charles'


def distance(A,B):
    x1, y1 = A.x, A.y
    x2, y2 = B.x, B.y
    d = sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))
    return [d, (x1-x2)/d, (y1-y2)/d]