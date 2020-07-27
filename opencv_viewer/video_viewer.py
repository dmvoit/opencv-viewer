from opencv_viewer.img_viewer import Viewer
import pathlib
import cv2
import sys
import numpy as np
import time


class VideoViewer(Viewer):

    @staticmethod
    def get_files_names(vid_file):
        path = pathlib.PosixPath(vid_file)
        if path.is_file() and path.suffix in ['.mp4', '.mp4']:
            return [vid_file]
        return ['']

    FRAME_LAST = None
    FRAME = None
    FRAME_COUNT = 0
    FRAME_POS = 0
    VIDEO_ENDED = False
    PLAY = True

    def set_window_title(self, path=None, data=''):
        if path is None:
            path = self.get_file_name(self.get_position_path())
        title = f'frame: {int(self.FRAME_POS):010}\t{path}  {data}'
        cv2.setWindowTitle(self.WINDOW, title)

    def resizeWindow(self, factor=1.0):
        if hasattr(self, 'FRAME') and self.FRAME is not None:
            w, h, c = np.shape(self.FRAME)
            cv2.resizeWindow(self.WINDOW, int(h * factor), int(w * factor))

    def play_video(self):
        cap = cv2.VideoCapture(self.paths[0])

        if (cap.isOpened() == False):
            print("Error opening video stream or file")
            sys.exit()

        self.FRAME_COUNT = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        if cap.isOpened():
            if self.FRAME is not None:
                self.FRAME_LAST = self.FRAME
            ret, self.FRAME = cap.read()
            print(ret)
            yield ret
        else:
            cap.release()
            self.VIDEO_ENDED = True
            yield False

    def vid_show(self):

        if self.paths == ['']:
            print('file not found')
            return

        self.generate_trackbar()

        cap = cv2.VideoCapture(self.paths[0])
        if (cap.isOpened() == False):
            print("Error opening video stream or file")
            sys.exit()

        self.FRAME_COUNT = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        while True:
            if self.FRAME is not None:
                self.FRAME_LAST = self.FRAME

            ret, self.FRAME = cap.read()
            self.FRAME_POS = cap.get(cv2.CAP_PROP_POS_FRAMES)

            time.sleep(0.05)

            if ret:
                w, h, c = np.shape(self.FRAME)
                cv2.imshow(self.WINDOW, self.FRAME)
                self.resizeWindow(factor=0.5)
                self.set_window_title()
                self.img_execute()

            self.key = cv2.waitKey(1)
            if self.key_pressed('q'):  # quit application
                break
            elif self.key_controller.key_pressed('r'): # restart
                self.FRAME_LAST = None
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            else:
                continue

        cap.release()
        cv2.destroyAllWindows()
