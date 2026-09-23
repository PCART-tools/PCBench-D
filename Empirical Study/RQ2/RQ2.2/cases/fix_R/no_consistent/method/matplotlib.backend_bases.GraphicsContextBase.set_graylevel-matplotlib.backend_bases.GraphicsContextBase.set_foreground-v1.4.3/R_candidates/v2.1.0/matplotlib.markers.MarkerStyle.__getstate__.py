    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_marker_function')
        return d
