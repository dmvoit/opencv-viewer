import cv2
import numpy as np


class KeyController:

    def __init__(self):
        self.key_registry = dict()

    def _verify_key(self, input):
        """

        :param input:
        :return: ( isVerified [bool], value [int])
        """
        if isinstance(input, str) and len(input) == 1:
            return True, ord(input)
        elif isinstance(input, int):
            return True, input
        else:
            return False, 0

    def key_pressed(self, input):

        is_verified, press = self._verify_key(input)
        if not is_verified:
            return False

        if hasattr(self, 'key') and self.key & 0xFF == press:
            self.key = -1  # resets key
            return True
        else:
            return False

    def _init_registry(self, input):
        if input not in self.key_registry:
            self.key_registry[input] = False

    def key_check(self, input):
        is_verified, key_num = self._verify_key(input)
        if not is_verified:
            return False

        self._init_registry(input)

        if self.key == key_num:
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
            if self.key_check('m'):
                print('checked')
            else:
                print(self.key)
            if self.key_pressed('q'):
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    controller = KeyController()
    controller.test_wait()
