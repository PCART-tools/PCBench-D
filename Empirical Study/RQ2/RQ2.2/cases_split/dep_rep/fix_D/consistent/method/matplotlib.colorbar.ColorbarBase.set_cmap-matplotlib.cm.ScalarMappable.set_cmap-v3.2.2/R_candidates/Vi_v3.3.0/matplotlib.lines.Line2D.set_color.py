    def set_color(self, color):
        """
        Set the color of the line.

        Parameters
        ----------
        color : color
        """
        self._color = color
        self.stale = True
