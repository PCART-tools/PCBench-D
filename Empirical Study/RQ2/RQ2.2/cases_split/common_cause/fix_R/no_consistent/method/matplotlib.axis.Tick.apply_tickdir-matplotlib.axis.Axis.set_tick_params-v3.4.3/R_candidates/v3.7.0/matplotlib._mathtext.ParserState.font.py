    @font.setter
    def font(self, name):
        if name in ('rm', 'it', 'bf'):
            self.font_class = name
        self._font = name
