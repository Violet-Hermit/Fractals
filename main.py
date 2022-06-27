import math
import time
import fractals
import keyboard as keyboard
from PIL import Image, ImageDraw


def write_prim(file, l):
    with open(file, 'r', encoding="utf8") as file_of_text:
        file_of_text.write(" ".join(list(map(str, l))))
        file_of_text.close()


def initialize_screen(wdh, hgh):
    global draw
    global im
    im = Image.new('RGB', (wdh, hgh), (255, 255, 255))
    draw = ImageDraw.Draw(im)


if __name__ == '__main__':
    initialize_screen(32000, 32000)
    exp = 10000
    # initialize_screen(2000, 2000)
    for i in fractals.do_mandelbrot(0, 0, 32000, 32000, exp):
        x1, y1, x2, y2, n = i
        # print(n)
        # (0, 0, 4000, 4000, -0.549653 + 0.003j, 5, 1000)
        # print(i[2])
        # color =(((i[2]/1000)**10*1920)**1.5) % 1920
        # if n == 0:
        #   n += 1
        r = (4 * n) % 255
        g = (6 * n) % 255
        b = (8 * n) % 255
        # color1 = int(abs(math.log10(n / exp)) * 255)
        # color2 = int(abs(math.log2(n / exp)) * 255)
        # color3 = int(abs(math.log1p(n / exp)) * 255)
        # s = n/1000
        # v = 1-math.pow(math.pi*s,2)
        # color = (int(75 - (75 * v)), int(28 + (75 - (75 * v))), int(math.pow(360 * s, 1.5) % 360))
        # print(color)
        draw.point(xy=((x1, y1), (x2, y2)),
                   fill=(r, g, b))
    # time.sleep(0.001)
    # write_prim('text.txt', l)
    print('fail')
    # draw.point(xy=tuple(l), fill='black')
    print('fail')
    im.show()
    im.save('draw-dots10.bmp', "BMP", quality=1000)
# 3:59-
