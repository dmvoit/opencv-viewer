class Trackbar:
    functions = {}

    def __init__(self, var_name, val=0, max=0):
        self.args = (var_name, val, max)

    def __call__(self, fn):
        (var_name, val, max) = self.args
        Trackbar.functions[var_name] = {'fn': fn, 'val': val, 'max': max}

        return fn


class Mouse:
    functions = []

    def __call__(self, fn):
        Mouse.functions.append(fn)
        return fn
