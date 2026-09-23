    def set_color(self, color):
        """
        Set the foreground color of the text

        Parameters
        ----------
        color : color
        """
        # Make sure it is hashable, or get_prop_tup will fail.
        try:
            hash(color)
        except TypeError:
            color = tuple(color)
        self._color = color
        self.stale = True
