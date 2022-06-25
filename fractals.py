import math
import time
from random import choice


def __init__(self, x, y):
    self.coord = (x, y)


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


def do_mandelbrot(x1, y1, x2, y2):
    for i in range(x2 - x1):
        for j in range(y2 - y1):
            if recurs(0, complex((4 * i) / ((x2 - x1)) - 2, (4 * j) / ((y2 - y1)) - 2),
                      100):  # some 'magic' numbers, they  are responsible for the considered part of the complex plane
                yield i, j


def recurs(z, c, n):
    n -= 1
    while n > 0:
        z = z * z + c
        if abs(z) > 2:
            return False
        if recurs(z, c, n):
            return True
        else:
            return False
    return True
