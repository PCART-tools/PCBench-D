    @allow_rasterization
    def draw(self, renderer):
        self._init()
        self.vector.draw(renderer)
        x, y = self.get_transform().transform_point((self.X, self.Y))
        self.text.set_x(self._text_x(x))
        self.text.set_y(self._text_y(y))
        self.text.draw(renderer)
        self.stale = False
