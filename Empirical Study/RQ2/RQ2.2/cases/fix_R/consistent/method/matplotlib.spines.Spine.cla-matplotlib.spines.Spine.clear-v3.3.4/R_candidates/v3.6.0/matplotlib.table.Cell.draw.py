    @allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            return
        # draw the rectangle
        super().draw(renderer)
        # position the text
        self._set_text_position(renderer)
        self._text.draw(renderer)
        self.stale = False
