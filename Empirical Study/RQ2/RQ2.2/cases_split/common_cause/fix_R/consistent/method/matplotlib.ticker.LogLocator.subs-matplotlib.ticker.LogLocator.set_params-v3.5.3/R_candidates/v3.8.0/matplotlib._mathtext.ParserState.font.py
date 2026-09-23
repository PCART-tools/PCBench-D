    @font.setter
    def font(self, name: str) -> None:
        if name in ('rm', 'it', 'bf', 'bfit'):
            self.font_class = name
        self._font = name
