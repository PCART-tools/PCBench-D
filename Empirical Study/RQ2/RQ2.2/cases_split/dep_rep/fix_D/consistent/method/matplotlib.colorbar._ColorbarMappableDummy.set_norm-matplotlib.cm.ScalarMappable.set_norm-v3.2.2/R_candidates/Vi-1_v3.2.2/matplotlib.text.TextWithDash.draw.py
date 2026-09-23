    def draw(self, renderer):
        """
        Draw the :class:`TextWithDash` object to the given *renderer*.
        """
        self.update_coords(renderer)
        Text.draw(self, renderer)
        if self.get_dashlength() > 0.0:
            self.dashline.draw(renderer)
        self.stale = False
