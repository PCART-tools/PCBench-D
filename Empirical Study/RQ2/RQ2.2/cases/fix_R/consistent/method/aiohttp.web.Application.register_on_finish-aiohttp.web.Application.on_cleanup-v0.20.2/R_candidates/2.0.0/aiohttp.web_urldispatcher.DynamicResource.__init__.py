    def __init__(self, pattern, formatter, *, name=None):
        super().__init__(name=name)
        assert pattern.pattern.startswith('\\/')
        assert formatter.startswith('/')
        self._pattern = pattern
        self._formatter = formatter
