import math
import time
import threading
import numpy as np
from numba import njit
from random import choice
from PIL import Image, ImageDraw

gradient = []


def do_polygon(k, l, coord):
    x, y = coord
    x1, y1 = x, y - l
    nodes = list()
    cos = math.cos(2 * math.pi / k)
    sin = math.sin(2 * math.pi / k)
    for i in range(k):
        nodes.append((math.floor(x + (x1 - x) * cos - (y1 - y) * sin), math.floor(y + (x1 - x) * sin + (y1 - y) * cos)))
        x1, y1 = nodes[-1]
    return nodes


def get_a_point_on_the_segment(pnt1, pnt2, numerator, denominator):  # get a point on line with coefficient
    x1, y1 = pnt1
    x2, y2 = pnt2
    return x1 + ((x2 - x1) * numerator // denominator), y1 + ((y2 - y1) * numerator // denominator)


def do_serp(nodes):
    pt = choice(nodes)
    while True:
        k = choice(nodes)
        pt = get_a_point_on_the_segment(k, pt, 1, 2)
        yield pt


def do_base_fractal(k, l, coord, numerator, denominator, time_to_exit):
    # k >= 5 numerator/denominator <= 1/2 , k = 3 numerator = 1 denominator = 2(Sierpinski triangle),
    # beautiful fractals are obtained with a ratio clos to 1/2
    nodes = do_polygon(k, l, coord)
    pt = choice(nodes)
    points = list()
    time2 = time.time()
    time1 = time.time()
    while True:
        if time1 - time2 > time_to_exit:
            return 0, 0
        time1 = time.time()
        k = choice(nodes)
        pt = get_a_point_on_the_segment(k, pt, numerator, denominator)
        if pt not in points:
            points.append(pt)
            time2 = time.time()
            yield pt


# I have many variants of fractals, but their code was written a long time ago and on pascal,
# so there are a lot of magic number there

def do_square_1(nodes):
    # you cannot select one node twice in a row
    pt = choice(nodes)
    k = choice(nodes)
    while True:
        t = nodes.copy()
        t.remove(k)
        k = choice(t)
        pt = get_a_point_on_the_segment(pt, k, 1, 2)
        yield pt


@njit(fastmath=True)
def do_mandelbrot(x1, y1, x2, y2, exp):
    for i in range(x2 - x1):
        #print(i)
        for j in range(math.floor((y2 - y1) / 2) + 1):
            yield i, j, i, y2 - j, check_for_occurrence(0, complex((3 * i) / (x2 - x1) - 2, (3 * j) / (y2 - y1) - 1.5),
                                                        2, exp)


def do_julia(x1, y1, x2, y2, c, exp, n):
    for i in range(x2 - x1 + 1):
        print(i)
        for j in range(y2 - y1 + 1):
            if check_for_occurrence(complex((2.3 * i) / (x2 - x1) - 1.1, (2.3 * j) / (y2 - y1) - 1.1), c, exp,
                                    n):
                # some 'magic' numbers, they  are responsible for the considered part of the complex plane
                yield i, j


# recurs(0, complex((3 * i) / ((x2 - x1)) - 2, (3 * j) / ((y2 - y1)) - 1.5), 100):

'''
def recurs(z, c, n):
    n -= 1
    while n > 0:
        z = z*z-0.2+0.75j
        if abs(z) > 5:  # <=> abs(z)>2, z.real*z.real + z.imag*z.imag > 4
            return False
        if recurs(z, c, n):
            return True
        else:
            return False
    return True
'''


@njit(fastmath=True, cache=True)
def check_for_occurrence(z, c, exp, n):  # z^5 - 0.549653 + 0.003j, beautiful
    x, y = z.real, z.imag
    if x >= math.sqrt((x - 0.25) * (x - 0.25) + y * y) - 2 * ((x - 0.25) * (x - 0.25) + y * y) + 0.25 or (x + 1) * (
            x + 1) + y * y <= 0.0625:
        return n
    k = 0
    for i in range(n):
        z = z * z + c
        if k == z:
            return n
        z = z * z + c
        k = z
        if z.real * z.real + z.imag * z.imag > 4:
            return i
    return n
# 2:35-3:23:16 48k:48k:1k
