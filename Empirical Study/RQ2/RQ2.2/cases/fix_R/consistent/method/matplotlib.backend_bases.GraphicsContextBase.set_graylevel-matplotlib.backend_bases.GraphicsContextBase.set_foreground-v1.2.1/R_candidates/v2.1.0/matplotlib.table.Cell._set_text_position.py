    def _set_text_position(self, renderer):
        """ Set text up so it draws in the right place.

        Currently support 'left', 'center' and 'right'
        """
        bbox = self.get_window_extent(renderer)
        l, b, w, h = bbox.bounds

        # draw in center vertically
        self._text.set_verticalalignment('center')
        y = b + (h / 2.0)

        # now position horizontally
        if self._loc == 'center':
            self._text.set_horizontalalignment('center')
            x = l + (w / 2.0)
        elif self._loc == 'left':
            self._text.set_horizontalalignment('left')
            x = l + (w * self.PAD)
        else:
            self._text.set_horizontalalignment('right')
            x = l + (w * (1.0 - self.PAD))

        self._text.set_position((x, y))
