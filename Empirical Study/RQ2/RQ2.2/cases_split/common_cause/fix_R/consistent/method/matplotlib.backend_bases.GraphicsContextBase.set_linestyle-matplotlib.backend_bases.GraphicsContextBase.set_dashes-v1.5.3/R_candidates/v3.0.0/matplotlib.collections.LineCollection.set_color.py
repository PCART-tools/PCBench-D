    def set_color(self, c):
        """
        Set the color(s) of the LineCollection.

        Parameters
        ----------
        c :
            Matplotlib color argument (all patches have same color), or a
            sequence or rgba tuples; if it is a sequence the patches will
            cycle through the sequence.
        """
        self.set_edgecolor(c)
        self.stale = True
