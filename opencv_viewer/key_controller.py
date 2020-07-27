import cv2
import numpy as np


def _covert_cahr_to_int_decorator(func):
    def wrapper(*args):
        if isinstance(args[1], int):
            return func(args[0], args[1])
        elif isinstance(args[1], str):
            return func(args[0], ord(args[1]))
        else:
            return False

    return wrapper


class KeyController:

    def __init__(self):
        self.key_registry = dict()


    @_covert_cahr_to_int_decorator
    def key_pressed(self, input):
        if hasattr(self, 'key') and self.key & 0xFF == input:
            self.key = -1  # resets key
            return True
        else:
            return False

    @_covert_cahr_to_int_decorator
    def key_check(self, input):

        if input not in self.key_registry:
            self.key_registry[input] = False

        if self.key == input:
            state = self.key_registry[input]
            self.key_registry[input] = not state
            if state:
                return state
            else:
                return self.key_registry[input]
        else:
            # last state
            return self.key_registry[input]

    def wait(self):
        self.key = cv2.waitKey(0)

    def test_wait(self):

        while True:
            cv2.imshow('w', np.zeros((100, 100)))
            self.key = cv2.waitKey(100)

            if self.key_pressed(32):
                print('press space')
                self.key = -1

            if self.key_check('m'):
                print('checked')
            else:
                print(self.key)
                # self._verify_key(1)
                # None
            if self.key_pressed('q'):
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    controller = KeyController()
    controller.test_wait()
