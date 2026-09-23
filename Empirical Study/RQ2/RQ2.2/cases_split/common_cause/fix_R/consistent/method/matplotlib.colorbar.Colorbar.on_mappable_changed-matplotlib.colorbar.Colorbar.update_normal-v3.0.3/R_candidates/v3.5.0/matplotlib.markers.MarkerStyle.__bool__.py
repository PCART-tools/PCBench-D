    def __bool__(self):
        return bool(len(self._path.vertices))
