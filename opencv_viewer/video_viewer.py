from opencv_viewer.img_viewer import Viewer
import pathlib
import cv2
import sys
import numpy as np
import time


class VideoViewer(Viewer):

    @staticmethod
    def get_files_names(root):
        path = pathlib.PosixPath(root)
        if path.is_file() and path.suffix in ['.mp4']:
            return [str(path)]
        file_paths = []
        for file in path.glob('*.mp4'):
            file_paths.append(str(file))
        return file_paths

    FRAME_LAST = None
    FRAME = None
    FRAME_COUNT = 0
    FRAME_POS = 0
    VIDEO_ENDED = False
    PLAY = True
    EXIT = False

    def set_window_title(self, path=None, data=''):
        if path is None:
            path = self.get_file_name(self.get_position_path())
        counter = self.position_counter()
        title = f'{counter} frame: {int(self.FRAME_POS):010}\t{path}  {data}'
        cv2.setWindowTitle(self.WINDOW, title)

    def resizeWindow(self, factor=1.0):
        if hasattr(self, 'FRAME') and self.FRAME is not None:
            w, h, c = np.shape(self.FRAME)
            cv2.resizeWindow(self.WINDOW, int(h * factor), int(w * factor))

    def vid_show(self):

        if len(self.paths) == 0:
            print('file not found')
            return

        self.generate_trackbar()

        while True:
            cap = cv2.VideoCapture(self.get_position_path())
            if (cap.isOpened() == False):
                print(f"Error opening {self.get_position_path()}")
                cv2.destroyAllWindows()
                sys.exit()

            self.FRAME_COUNT = cap.get(cv2.CAP_PROP_FRAME_COUNT)

            while True:
                self.FRAME_POS = cap.get(cv2.CAP_PROP_POS_FRAMES)
                if self.FRAME_POS > 0:
                    self.FRAME_LAST = self.FRAME

                if self.PLAY:
                    ret, self.FRAME = cap.read()

                time.sleep(0.05)

                if self.FRAME is not None:
                    cv2.imshow(self.WINDOW, self.FRAME)
                    self.resizeWindow(factor=0.5)
                    self.set_window_title()
                    self.img_execute()

                self.key_controller.wait(time=1)

                self.PLAY = not self.key_controller.key_check(32)  # pause with space

                if self.key_controller.key_pressed('q'):  # quit application
                    self.EXIT = True
                    break
                elif self.key_controller.key_pressed(83):  # next video arrow ->
                    self.move_to_next_path()
                    break
                elif self.key_controller.key_pressed(81):  # prev video arrow <-
                    self.move_to_prev_path()
                    break
                elif self.key_controller.key_pressed('+') and not self.PLAY:
                    self.PLAY = True
                elif self.key_controller.key_pressed('-') and not self.PLAY:
                    if self.FRAME_POS != 0:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, self.FRAME_POS-2)
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
