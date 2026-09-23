    def _approx_text_height(self, renderer=None):
        """
        Return the approximate height of the text. This is used to place
        the legend handle.
        """
        if renderer is None:
            return self._fontsize
        else:
            return renderer.points_to_pixels(self._fontsize)
