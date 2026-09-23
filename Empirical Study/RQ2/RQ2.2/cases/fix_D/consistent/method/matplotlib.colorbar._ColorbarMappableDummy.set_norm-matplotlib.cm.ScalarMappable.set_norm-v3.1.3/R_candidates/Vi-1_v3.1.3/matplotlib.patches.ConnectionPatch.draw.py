    def draw(self, renderer):
        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible() or not self._check_xy(renderer):
            return
        FancyArrowPatch.draw(self, renderer)
