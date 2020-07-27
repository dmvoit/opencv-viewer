import cv2
import os


class Viewer:
    WINDOW = "window"

    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (0, 0, 255)
    COLOR_BLUE = (255, 0, 0)
    COLOR_CYAN = (255, 255, 0)
    COLOR_MAGENTA = (255, 0, 255)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)

    position = 0

    def __init__(self, path):
        self.paths = self.get_files_names(path)
        self.paths.sort()
        self.n_paths = len(self.paths)
        cv2.namedWindow(self.WINDOW, cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_EXPANDED)

    @staticmethod
    def get_files_names(root_dir):
        file_paths = []

        for file in os.listdir(root_dir):
            if file.endswith(tuple(['.JPG', '.jpg', '.PNG', '.png'])):
                file_paths.append(f"{root_dir}/{file}")
        return file_paths

    def get_param_str(self):
        if hasattr(self, 'PARAMS'):
            param = getattr(self, 'PARAMS')
            return " ".join(sorted([f"{key}:{param[key]['val']} " for key in param.keys()]))
        else:
            return ""

    def get_position_path(self, offset=0):
        return self.paths[self.position + offset]

    def move_to_next_path(self):
        self.position += 1
        self.position %= self.n_paths

    # def generate_trackbar(self):
    #     pass

    def img_execute(self):
        pass

    def img_show(self):

        if self.n_paths < 1:
            return

        if hasattr(self, 'PARAMS'):
            params = getattr(self, 'PARAMS')
            for method_name in dir(self):
                if method_name.startswith("on_trackbar"):
                    var_name = method_name.split('_')[-1]
                    cv2.createTrackbar(var_name, self.WINDOW,
                                       params[var_name]['val'], params[var_name]['max'],
                                       getattr(self, method_name))

        while True:
            self.img = cv2.imread(self.get_position_path())
            self.img = cv2.resize(self.img, None, fx=0.50, fy=0.50, interpolation=cv2.INTER_AREA)

            cv2.imshow(self.WINDOW, self.img)
            cv2.resizeWindow(self.WINDOW, int(self.img.shape[1] / 1), int(self.img.shape[0] / 1))
            cv2.setWindowTitle(self.WINDOW, self.get_position_path())
            self.img_execute()

            self.key = cv2.waitKey(0)
            if self.key & 0xFF == ord('q'):  # quit application
                break
            elif self.key & 0xFF == ord('r'):  # reload image
                continue
            elif self.key & 0xFF == ord('+'):  # next image
                self.move_to_next_path()
                continue
        cv2.destroyAllWindows()
