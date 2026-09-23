        def __nonzero__(self):
            return bool(len(self._path.vertices))
