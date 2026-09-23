    def __init__(self, values, index, name, orig=None):
        self.values = values
        self.index = index
        self.name = name
        self.orig = orig
        self._freeze()
