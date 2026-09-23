    def add_prefix(self, prefix):
        assert prefix.startswith('/')
        assert not prefix.endswith('/')
        assert len(prefix) > 1
        self._path = prefix + self._path
