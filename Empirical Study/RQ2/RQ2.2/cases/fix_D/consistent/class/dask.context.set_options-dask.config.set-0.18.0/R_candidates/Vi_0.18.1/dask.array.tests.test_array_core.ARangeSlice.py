    class ARangeSlice(object):
        def __init__(self, start, stop):
            self.start = start
            self.stop = stop

        def __array__(self):
            return np.arange(self.start, self.stop)
