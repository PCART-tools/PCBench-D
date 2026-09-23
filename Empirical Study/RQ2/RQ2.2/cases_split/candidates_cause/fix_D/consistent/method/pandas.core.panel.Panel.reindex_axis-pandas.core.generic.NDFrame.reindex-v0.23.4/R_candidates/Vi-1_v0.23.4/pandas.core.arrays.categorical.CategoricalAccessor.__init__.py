    def __init__(self, data):
        self._validate(data)
        self.categorical = data.values
        self.index = data.index
        self.name = data.name
        self._freeze()
