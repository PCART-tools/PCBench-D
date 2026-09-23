    def __setstate__(self, state):
        path, size, index, encoding, layout_engine = state
        self.__init__(path, size, index, encoding, layout_engine)
