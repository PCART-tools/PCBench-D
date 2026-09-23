    def __exit__(self, *args):
        dict.update(rcParams, self._orig)
