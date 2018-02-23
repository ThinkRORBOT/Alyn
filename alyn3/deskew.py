""" Deskews file after getting skew angle """
import optparse
import numpy as np
import math
import matplotlib.pyplot as plt

from .skew_detect import SkewDetect
from skimage import io
from skimage.transform import rotate


class Deskew:

    def __init__(self, input_file, display_image, crop_image, output_file, r_angle, max_angle = 90.0):

        self.input_file = input_file
        self.display_image = display_image
        self.crop_image = crop_image
        self.output_file = output_file
        self.r_angle = r_angle
        self.max_angle=max_angle
        self.skew_obj = SkewDetect(self.input_file)

    def deskew(self):

        img = io.imread(self.input_file)
        res = self.skew_obj.process_single_file()
        angle = res['Estimated Angle']

        rot_angle = 0

        if angle >= 0 and angle <= 90:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -45 and angle < 0:
            rot_angle = angle - 90 + self.r_angle
        if angle >= -90 and angle < -45:
            rot_angle = 90 + angle + self.r_angle

        negativeAngle = False
        if rot_angle < 0:
            negativeAngle = True
        if abs(rot_angle) > abs(self.max_angle):
            rot_angle = rot_angle%self.max_angle
            if negativeAngle:
                rot_angle = -rot_angle

        rotated = rotate(img, rot_angle, resize=True)

        if self.display_image:
            try:
                self.display(rotated)
            except:
                print("Display Error")

        if self.crop_image:
            imageHeight, imageWidth = rotated.shape[:2]
            #print(rotated.shape)
            rot_angle = abs(rot_angle)
            rot_angle = rot_angle%90
            if rot_angle > 45:
                rot_angle = 90 - rot_angle
            radianAngle = math.radians(rot_angle)
            oppositeSide = abs(math.tan(radianAngle) * imageWidth)
            oppositeSide2 = abs(math.tan(radianAngle) * imageHeight)
            if oppositeSide > imageHeight / 2 or oppositeSide2 > imageWidth/2 or abs(rot_angle) > 20:
                print("Not Cropping Image")
            else:
                print(imageHeight, oppositeSide, imageWidth, oppositeSide2, rot_angle)
                rotated = rotated[int(oppositeSide): 0 + int(imageHeight - oppositeSide), int(oppositeSide2): 0 + int(imageWidth - oppositeSide2)]

        if self.output_file:
            self.saveImage(rotated*255)

    def saveImage(self, img):
        path = self.skew_obj.check_path(self.output_file)
        io.imsave(path, img.astype(np.uint8))


    def display(self, img):

        plt.imshow(img)
        plt.show()

    def run(self):
        angle = 0
        if self.input_file:
             self.deskew()


if __name__ == '__main__':

    parser = optparse.OptionParser()

    parser.add_option(
        '-i',
        '--input',
        default=None,
        dest='input_file',
        help='Input file name')
    parser.add_option(
        '-d', '--display',
        default=None,
        dest='display_image',
        help="display the rotated image")
    parser.add_option(
        '-o', '--output',
        default=None,
        dest='output_file',
        help='Output file name')
    parser.add_option(
        '-r', '--rotate',
        default=0,
        dest='r_angle',
        help='Rotate the image to desired axis',
        type=int)
    options, args = parser.parse_args()
    deskew_obj = Deskew(
        options.input_file,
        options.display_image,
        options.crop_image,
        options.output_file,
        options.r_angle)

    deskew_obj.run()
