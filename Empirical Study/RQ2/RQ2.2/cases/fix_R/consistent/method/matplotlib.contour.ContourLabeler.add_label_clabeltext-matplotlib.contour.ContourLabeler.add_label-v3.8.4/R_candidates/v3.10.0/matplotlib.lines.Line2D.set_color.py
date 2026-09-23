    def set_color(self, color):
        """
        Set the color of the line.

        Parameters
        ----------
        color : :mpltype:`color`
        """
        mcolors._check_color_like(color=color)
        self._color = color
        self.stale = True
