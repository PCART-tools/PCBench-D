    @property
    def size(self):
        try:
            return os.fstat(self._value.fileno()).st_size - self._value.tell()
        except OSError:
            return None
