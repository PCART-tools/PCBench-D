    def get_paths(self):
        if self._paths is None:
            self.set_paths()
        return self._paths
