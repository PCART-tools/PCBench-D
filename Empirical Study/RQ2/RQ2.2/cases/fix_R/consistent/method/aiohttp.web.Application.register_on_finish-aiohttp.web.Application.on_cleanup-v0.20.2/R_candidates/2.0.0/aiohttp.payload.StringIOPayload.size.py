    @property
    def size(self):
        return len(self._value.getvalue()) - self._value.tell()
