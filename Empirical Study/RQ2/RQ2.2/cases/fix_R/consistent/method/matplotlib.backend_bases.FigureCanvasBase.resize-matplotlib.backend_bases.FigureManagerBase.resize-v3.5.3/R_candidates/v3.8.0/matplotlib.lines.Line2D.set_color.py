    def set_color(self, color):
        """
        Set the color of the line.

        Parameters
        ----------
        color : color
        """
        mcolors._check_color_like(color=color)
        self._color = color
        self.stale = True
