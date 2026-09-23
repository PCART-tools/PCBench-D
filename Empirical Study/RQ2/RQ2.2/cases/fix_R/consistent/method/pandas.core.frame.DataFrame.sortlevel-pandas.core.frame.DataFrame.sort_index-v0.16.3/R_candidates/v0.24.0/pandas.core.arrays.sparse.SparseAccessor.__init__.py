    def __init__(self, data=None):
        self._validate(data)
        # Store the Series since we need that for to_coo
        self._parent = data
