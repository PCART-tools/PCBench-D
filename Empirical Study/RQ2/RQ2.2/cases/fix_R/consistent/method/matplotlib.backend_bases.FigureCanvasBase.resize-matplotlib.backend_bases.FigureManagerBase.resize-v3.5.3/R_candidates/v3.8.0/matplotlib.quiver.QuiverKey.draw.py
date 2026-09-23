    @martist.allow_rasterization
    def draw(self, renderer):
        self._init()
        self.vector.draw(renderer)
        pos = self.get_transform().transform((self.X, self.Y))
        self.text.set_position(pos + self._text_shift())
        self.text.draw(renderer)
        self.stale = False
