    @property
    def size(self):
        p = self._value.tell()
        l = self._value.seek(0, os.SEEK_END)
        self._value.seek(p)
        return l - p
