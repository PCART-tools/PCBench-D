    def set_color(self, c):
        """
        Set the color(s) of the LineCollection.

        Parameters
        ----------
        c : color or list of colors
            Single color (all patches have same color), or a
            sequence of rgba tuples; if it is a sequence the patches will
            cycle through the sequence.
        """
        self.set_edgecolor(c)
        self.stale = True
