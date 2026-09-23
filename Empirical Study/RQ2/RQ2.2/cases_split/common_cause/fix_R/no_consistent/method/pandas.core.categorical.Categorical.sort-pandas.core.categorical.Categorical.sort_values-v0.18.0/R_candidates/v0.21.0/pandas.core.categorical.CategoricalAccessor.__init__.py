    def __init__(self, values, index, name):
        self.categorical = values
        self.index = index
        self.name = name
        self._freeze()
