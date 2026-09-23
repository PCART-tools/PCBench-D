    def __init__(self, prefix, *, name=None):
        assert not prefix or prefix.startswith('/'), prefix
        assert prefix in ('', '/') or not prefix.endswith('/'), prefix
        super().__init__(name=name)
        self._prefix = URL(prefix).raw_path
