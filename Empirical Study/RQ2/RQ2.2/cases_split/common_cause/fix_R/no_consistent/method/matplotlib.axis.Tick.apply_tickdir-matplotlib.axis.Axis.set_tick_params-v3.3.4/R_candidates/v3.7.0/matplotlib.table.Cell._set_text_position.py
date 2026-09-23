    def _set_text_position(self, renderer):
        """Set text up so it is drawn in the right place."""
        bbox = self.get_window_extent(renderer)
        # center vertically
        y = bbox.y0 + bbox.height / 2
        # position horizontally
        loc = self._text.get_horizontalalignment()
        if loc == 'center':
            x = bbox.x0 + bbox.width / 2
        elif loc == 'left':
            x = bbox.x0 + bbox.width * self.PAD
        else:  # right.
            x = bbox.x0 + bbox.width * (1 - self.PAD)
        self._text.set_position((x, y))
