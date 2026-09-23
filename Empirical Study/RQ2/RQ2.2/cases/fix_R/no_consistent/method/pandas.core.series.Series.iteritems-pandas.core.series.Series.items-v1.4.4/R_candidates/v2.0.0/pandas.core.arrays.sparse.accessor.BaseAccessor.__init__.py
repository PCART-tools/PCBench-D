    def __init__(self, data=None) -> None:
        self._parent = data
        self._validate(data)
