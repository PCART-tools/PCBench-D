    @property
    def size(self):
        return len(self._value.getbuffer()) - self._value.tell()
