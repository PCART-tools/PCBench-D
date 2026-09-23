    def get_path(self):
        if self._path is None:
            self._recompute_path()
        return self._path
