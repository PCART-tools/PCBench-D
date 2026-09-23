    def __init__(self, path, *, name=None):
        super().__init__(name=name)
        assert not path or path.startswith('/')
        self._path = path
