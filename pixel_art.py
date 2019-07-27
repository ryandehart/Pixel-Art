import cv2
import math
import numpy as np
import random
import copy

img = cv2.imread('temp.png')

#-Combine pixels
size = 6
pixels = []
factor = 16
for i in range(0, len(img), size):
    print("pixelizing row " + str(i) + " out of " + str(len(img)), end='\r')
    pixels.append([])
    for j in range(0, len(img[i]), size):
        pixels[int(i / size)].append([])

        average = [0, 0, 0]
        for a in range(0, size):
            ip1 = min(i + a, len(img) - 1)
            for b in range(0, size):
                jp1 = min(j + b, len(img[i]) - 1)

                for c in range(0, 3):
                    average[c] += int(img[ip1][jp1][c])

        for c in range(0, 3):
            average[c] /= size ** 2

        pixels[int(i / size)][int(j / size)] = average

        flr = [math.floor(x / factor) * factor for x in pixels[int(i / size)][int(j / size)]]
        diff = []
        for c in range(0, len(flr)):
            diff.append(img[i][j][c] - flr[c])

        for c in range(0, len(flr)):
            if (random.random() > diff[c] / (256 / factor)):
                pixels[int(i / size)][int(j / size)][c] = math.floor(pixels[int(i / size)][int(j / size)][c] / factor) * factor
            else:
                pixels[int(i / size)][int(j / size)][c] = min(255, math.ceil(pixels[int(i / size)][int(j / size)][c] / factor) * factor)
print("")

#-Outlines
outlined = copy.deepcopy(pixels)
for i in range(0, len(pixels)):
    print("outlining row " + str(i) + " out of " + str(len(pixels)), end='\r')
    for j in range(0, len(pixels[i])):
        im1 = max(0, i - 1)
        ip1 = min(len(pixels) - 1, i + 1)
        jm1 = max(0, j - 1)
        jp1 = min(len(pixels[i]) - 1, j + 1)

        diff = 0
        for c in range(0, 3):
            diff += pixels[im1][j][c] - pixels[i][j][c]
            diff += pixels[ip1][j][c] - pixels[i][j][c]
            diff += pixels[i][jm1][c] - pixels[i][j][c]
            diff += pixels[i][jp1][c] - pixels[i][j][c]

        t = 2
        m = abs(int(float(diff) / (t * 1.8 * factor)))
        if (diff > t * factor):
            for c in range(0, 3):
                outlined[i][j][c] = max(0, pixels[i][j][c] - m * factor)
        elif(-1 * diff > t * factor):
            for c in range(0, 3):
                outlined[i][j][c] = min(255, pixels[i][j][c] + m * factor)


print("")

#-Reduce number of colors
for i in range(0, len(img)):
    print("generating row " + str(i) + " out of " + str(len(img)), end='\r')
    for j in range(0, len(img[i])):
        img[i][j] = [x for x in outlined[int(i / size)][int(j / size)]]
print("")

cv2.imwrite('background.png',img)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
