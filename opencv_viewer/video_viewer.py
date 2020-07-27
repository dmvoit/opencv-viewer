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
    VIDEO_ENDED = False

    def play_video(self):
        cap = cv2.VideoCapture(self.paths[0])

        if (cap.isOpened() == False):
            print("Error opening video stream or file")
            sys.exit()

        self.FRAME_COUNT = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        if cap.isOpened():
            # cap.get(cv2.CAP_PROP_)
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

            time.sleep(0.05)

            if ret:
                w, h, c = np.shape(self.FRAME)
                cv2.imshow(self.WINDOW, self.FRAME)
                factor = 2
                cv2.resizeWindow(self.WINDOW, int(h/ factor), int(w / factor))
                cv2.setWindowTitle(self.WINDOW, self.get_position_path())
                self.img_execute()

            self.key = cv2.waitKey(1)
            if self.key_pressed('q'):  # quit application
                break
            elif self.key_pressed('p'):
                cv2.waitKey(-1)
            elif self.key_pressed('r'):
                self.FRAME_LAST = None
                self.FRAME = None
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            else:
                continue

        cap.release()
        cv2.destroyAllWindows()
