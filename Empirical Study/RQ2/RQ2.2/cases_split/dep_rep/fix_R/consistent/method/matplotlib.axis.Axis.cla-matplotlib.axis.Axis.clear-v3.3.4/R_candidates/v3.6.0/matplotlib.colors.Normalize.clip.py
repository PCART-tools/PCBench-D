    @clip.setter
    def clip(self, value):
        if value != self._clip:
            self._clip = value
            self._changed()
