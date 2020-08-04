from opencv_viewer.img_viewer import Viewer
import cv2
import numpy as np
import time


class VideoViewer(Viewer):

    @staticmethod
    def get_files_names(root, suffix=None):
        if suffix is None:
            suffix = ['mp4']
        return Viewer.get_files_names(root, suffix)

    FRAME_LAST = None
    FRAME = None
    FRAME_COUNT = 0
    FRAME_POS = 0
    VIDEO_ENDED = False
    PLAY = True
    EXIT = False
    NEXT_FILE = False

    def set_window_title(self, path=None, data=''):
        if path is None:
            path = self.get_file_name(self.get_position_path())
        counter = self.position_counter()
        title = f'{counter} frame: {int(self.FRAME_POS):010}\t{path}  {data}'
        cv2.setWindowTitle(self.WINDOW, title)

    def resizeWindow(self, factor=None):  # TODO last frame resize
        if factor is None:
            factor = self.DEFAULT_FACTOR
        if hasattr(self, 'FRAME') and self.FRAME is not None:
            shape = np.shape(self.FRAME)
            cv2.resizeWindow(self.WINDOW, int(shape[1] * factor), int(shape[0] * factor))

    def vid_show(self):

        self.generate_trackbar()

        while True:
            cap = cv2.VideoCapture(self.get_position_path())
            if (cap.isOpened() == False):
                cv2.destroyAllWindows()
                raise Exception(f"Error opening: {self.get_position_path()}")

            self.FRAME_COUNT = cap.get(cv2.CAP_PROP_FRAME_COUNT)

            while True:
                self.FRAME_POS = cap.get(cv2.CAP_PROP_POS_FRAMES)
                if self.FRAME_POS > 0 and self.FRAME is not None:
                    self.FRAME_LAST = self.FRAME

                if self.PLAY:
                    ret, self.FRAME = cap.read()

                time.sleep(0.05)

                if self.FRAME is not None:
                    cv2.imshow(self.WINDOW, self.FRAME)
                    self.resizeWindow()
                    self.set_window_title()
                    self.img_execute(next=self.NEXT_FILE)
                    if self.NEXT_FILE is True:
                        self.NEXT_FILE = False
                elif self.FRAME_LAST is not None:
                    cv2.imshow(self.WINDOW, self.FRAME_LAST)
                    self.resizeWindow()
                    self.set_window_title()

                self.key_controller.wait(time=1)
                self.PLAY = not self.key_controller.key_check(32)  # pause with space

                if self.key_controller.key_pressed('q'):  # quit application
                    self.EXIT = True
                    break
                elif self.key_controller.key_pressed(83):  # next video arrow ->
                    self.move_to_next_path()
                    self.PLAY = True
                    self.NEXT_FILE = True
                    break
                elif self.key_controller.key_pressed(81):  # prev video arrow <-
                    self.move_to_prev_path()
                    self.PLAY = True
                    self.NEXT_FILE = True
                    break
                elif self.key_controller.key_pressed(82):
                    self.DEFAULT_FACTOR += 0.1
                elif self.key_controller.key_pressed(84):
                    self.DEFAULT_FACTOR -= 0.1
                elif self.key_controller.key_pressed('+') and not self.PLAY:
                    self.PLAY = True
                elif self.key_controller.key_pressed('-') and not self.PLAY:
                    if self.FRAME_POS != 0:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, self.FRAME_POS - 2)
                        self.PLAY = True
                elif self.key_controller.key_pressed('r'):  # restart
                    self.FRAME_LAST = None
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    self.PLAY = True
                else:
                    continue

            self.FRAME_POS = 0
            self.FRAME_LAST = None

            cap.release()

            if self.EXIT is True:
                break
        cv2.destroyAllWindows()
