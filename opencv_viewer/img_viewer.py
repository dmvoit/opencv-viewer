from opencv_viewer.key_controller import KeyController
from opencv_viewer.gui_decorators import Trackbar, Mouse
import cv2
import pathlib


class Viewer:
    WINDOW = "opencv_viewer"

    COLOR_GREEN = (0, 255, 0)
    COLOR_RED = (0, 0, 255)
    COLOR_BLUE = (255, 0, 0)
    COLOR_CYAN = (255, 255, 0)
    COLOR_MAGENTA = (255, 0, 255)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)

    DEFAULT_FACTOR = 0.5

    def __init__(self, path):
        self.paths = self.get_files_names(path)
        self.position = 0

        self.n_paths = len(self.paths)

        self.key_controller = KeyController()
        self.params_trackbar = Trackbar.functions
        self.mouse_functions = Mouse.functions

        cv2.namedWindow(self.WINDOW,
                        cv2.WINDOW_GUI_NORMAL |
                        cv2.WINDOW_NORMAL |
                        cv2.WINDOW_KEEPRATIO )

    @staticmethod
    def get_files_names(root, suffix=None):
        if suffix is None:
            suffix = ['jpg', 'png']

        suffix = [ext if ext.startswith('.') else '.' + ext for ext in suffix]
        # glob is case insensitive in  python 3.10
        # suffix_upper = [ext.upper() for ext in suffix]
        # suffix = list(set(suffix).union(set(suffix_upper)))

        path = pathlib.Path(root)
        if path.is_file() and path.suffix in suffix:
            return [str(path)]

        if not path.is_dir():
            raise Exception(f'file not found/wrong file type: {path.absolute()}')

        file_paths = []
        for ext in suffix:
            for file in path.glob('*' + ext):
                file_paths.append(str(file))

        if len(file_paths) < 1:
            raise Exception(f'no files found: {path.absolute()}')

        file_paths.sort()
        return file_paths

    def get_param_str(self):
        if hasattr(self, 'PARAMS'):
            param = getattr(self, 'PARAMS')
            return " ".join(sorted([f"{key}:{param[key]['val']} " for key in param.keys()]))
        else:
            return ""

    def get_position_path(self, offset=0):
        return self.paths[self.position + offset]

    @staticmethod
    def get_file_name(path):
        return path.split('/')[-1]

    def position_counter(self):
        if self.n_paths > 1:
            return f'[{self.position + 1:03}/{self.n_paths:03}]'
        else:
            return ''

    def set_window_title(self, path=None, data=''):

        counter = self.position_counter()

        if path is None:
            path = self.get_file_name(self.get_position_path())
        title = f'{counter} {path}  {data}'
        cv2.setWindowTitle(self.WINDOW, title)

    def move_to_next_path(self):
        self.position += 1
        self.position %= self.n_paths

    def move_to_prev_path(self):
        self.position -= 1
        self.position %= self.n_paths

    def gen_gui(self):
        params =self.params_trackbar
        for var_name in params.keys():
            cv2.createTrackbar(var_name, self.WINDOW,
                               params[var_name]['val'],
                               params[var_name]['max'],
                               params[var_name]['fn'].__get__(self, self.__class__))
        # params[var_name]['fn'].__get__(self, self.__class__) make method bound
        # https://stackoverflow.com/questions/1015307/

        for fn in self.mouse_functions:
            cv2.setMouseCallback(self.WINDOW, fn.__get__(self, self.__class__))


    def resize(self, img, factor=0.5):
        return cv2.resize(img, None, fx=factor, fy=factor, interpolation=cv2.INTER_AREA)

    def resizeWindow(self, factor=None):
        if factor is None:
            factor = self.DEFAULT_FACTOR
        if hasattr(self, 'img'):
            cv2.resizeWindow(self.WINDOW, int(self.img.shape[1] * factor), int(self.img.shape[0] * factor))

    def img_execute(self, **kwargs):
        pass

    def pre_execute(self, **kwargs):
        pass

    def post_execute(self, **kwargs):
        pass

    def img_show(self):

        self.pre_execute()
        self.gen_gui()


        while True:
            self.img = cv2.imread(self.get_position_path())
            self.img = self.resize(self.img)

            cv2.imshow(self.WINDOW, self.img)
            self.resizeWindow()

            self.set_window_title()
            self.img_execute()

            self.key_controller.wait()
            if self.key_controller.key_pressed('q'):  # quit application
                break
            elif self.key_controller.key_pressed('r'):  # reload image
                continue
            elif self.key_controller.key_pressed(82):
                self.DEFAULT_FACTOR += 0.1
            elif self.key_controller.key_pressed(84):
                self.DEFAULT_FACTOR -= 0.1
            elif self.key_controller.key_pressed('+'):  # next image
                self.move_to_next_path()
                continue
            elif self.key_controller.key_pressed('-'):  # next image
                self.move_to_prev_path()
                continue

        self.post_execute()
        cv2.destroyAllWindows()
