import cv2
import numpy as np


def _covert_char_to_int_decorator(func):
    def wrapper(*args):
        if isinstance(args[1], int):
            return func(*args)
        elif isinstance(args[1], str):
            ar = list(args)
            ar[1] = ord(args[1])
            return func(*tuple(ar))
        else:
            return False

    return wrapper


class KeyController:

    def __init__(self):
        self.key_registry = dict()
        self.option_registry = dict()

    @_covert_char_to_int_decorator
    def key_pressed(self, input):
        if hasattr(self, 'key') and self.key & 0xFF == input:
            self.key = -1  # resets key
            return True
        else:
            return False

    @_covert_char_to_int_decorator
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

    @_covert_char_to_int_decorator
    def key_option(self, input, options):

        if input not in self.option_registry:
            self.option_registry[input] = {'len': len(options), 'pos': 0}

        if self.key == input:
            state = self.option_registry[input]

            state['pos'] += 1
            state['pos'] %= state['len']

            return options[self.option_registry[input]['pos']]
        else:
            # last state
            return options[self.option_registry[input]['pos']]

    def wait(self, time=0):
        self.key = cv2.waitKey(time)

    def test_wait(self):

        while True:
            cv2.imshow('w', np.zeros((100, 100)))
            # self.key = cv2.waitKey(-1)
            self.wait(100)

            if self.key_pressed(32):
                print('press space')
                self.key = -1

            if self.key_check('m'):
                print('checked')
            else:
                print(self.key)
                # print(self.key_option('o',['ap','bd','re']))
                # self._verify_key(1)
            if self.key_pressed('q'):
                break
        cv2.destroyAllWindows()


if __name__ == '__main__':
    controller = KeyController()
    controller.test_wait()
