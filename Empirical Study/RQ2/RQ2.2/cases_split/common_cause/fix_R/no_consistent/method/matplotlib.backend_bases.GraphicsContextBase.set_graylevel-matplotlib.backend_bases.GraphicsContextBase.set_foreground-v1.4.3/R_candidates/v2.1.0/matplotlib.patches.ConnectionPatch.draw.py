    def draw(self, renderer):
        """
        Draw.
        """

        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible():
            return

        if not self._check_xy(renderer):
            return

        FancyArrowPatch.draw(self, renderer)
