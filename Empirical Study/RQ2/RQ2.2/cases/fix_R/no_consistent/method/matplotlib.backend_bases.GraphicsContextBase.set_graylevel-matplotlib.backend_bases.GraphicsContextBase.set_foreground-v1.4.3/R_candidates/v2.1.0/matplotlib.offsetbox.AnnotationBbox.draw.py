    def draw(self, renderer):
        """
        Draw the :class:`Annotation` object to the given *renderer*.
        """

        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible():
            return

        xy_pixel = self._get_position_xy(renderer)

        if not self._check_xy(renderer, xy_pixel):
            return

        self.update_positions(renderer)

        if self.arrow_patch is not None:
            if self.arrow_patch.figure is None and self.figure is not None:
                self.arrow_patch.figure = self.figure
            self.arrow_patch.draw(renderer)

        if self._drawFrame:
            self.patch.draw(renderer)

        self.offsetbox.draw(renderer)
        self.stale = False
