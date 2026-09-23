    def set_color(self, color):
        """
        Set the foreground color of the text

        Parameters
        ----------
        color : color
        """
        # "auto" is only supported by axisartist, but we can just let it error
        # out at draw time for simplicity.
        if not cbook._str_equal(color, "auto"):
            mpl.colors._check_color_like(color=color)
        # Make sure it is hashable, or get_prop_tup will fail (remove this once
        # get_prop_tup is removed).
        try:
            hash(color)
        except TypeError:
            color = tuple(color)
        self._color = color
        self.stale = True
