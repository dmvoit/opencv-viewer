import cv2

from opencv_viewer.img_viewer import Viewer
from opencv_viewer.gui_decorators import Trackbar, Mouse
import numpy as np


class RGBTrackbar(Viewer):
    PARAMS = {
        'r': {'val': 127},
        'g': {'val': 127},
        'b': {'val': 127}
    }

    def resizeWindow(self, factor=3):
        return super().resizeWindow(factor)

    @Trackbar('r', 127, 255)
    def color(self, val):
        self.PARAMS['r']['val'] = val
        if hasattr(self,'img'):
            self.img_execute()

    @Trackbar('g', 127, 255)
    def color_g(self, val):
        self.PARAMS['g']['val'] = val
        if hasattr(self, 'img'):
            self.img_execute()

    @Trackbar('b', 127, 255)
    def color_b(self, val):
        self.PARAMS['b']['val'] = val
        if hasattr(self, 'img'):
            self.img_execute()

    @Mouse()
    def get_color_value(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.set_window_title(data=f" x={x:3} ,y={y:3} - bgr:{self.img_temp[y, x] if hasattr(self,'img_temp') else self.img[y, x]} ")

    def img_execute(self):

        temp = self.img.copy()

        [blue, green, red] = cv2.split(temp.astype(np.int32))

        self.color_diff(red, self.PARAMS['r'])
        self.color_diff(green, self.PARAMS['g'])
        self.color_diff(blue, self.PARAMS['b'])

        self.img_temp = cv2.merge((blue, green, red)).astype(np.uint8)

        cv2.imshow(self.WINDOW, self.img_temp)

    def color_diff(self, color, selection):
        color+=np.dtype('int32').type(selection['val'] - 127)
        color[color<0] = 0
        color[color>255] = 255


if __name__ == '__main__':
    viewer = RGBTrackbar('../media/photo')
    viewer.img_show()
