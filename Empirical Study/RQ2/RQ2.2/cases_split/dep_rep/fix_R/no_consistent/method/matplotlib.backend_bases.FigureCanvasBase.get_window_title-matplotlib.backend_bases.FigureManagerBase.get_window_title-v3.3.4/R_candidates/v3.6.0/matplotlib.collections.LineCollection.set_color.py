    def set_color(self, c):
        """
        Set the edgecolor(s) of the LineCollection.

        Parameters
        ----------
        c : color or list of colors
            Single color (all lines have same color), or a
            sequence of rgba tuples; if it is a sequence the lines will
            cycle through the sequence.
        """
        self.set_edgecolor(c)
