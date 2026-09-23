    def arc(self, xy, start, end, fill=None, width=1):
        """Draw an arc."""
        ink, fill = self._getink(fill)
        if ink is not None:
            self.draw.draw_arc(xy, start, end, ink, width)
