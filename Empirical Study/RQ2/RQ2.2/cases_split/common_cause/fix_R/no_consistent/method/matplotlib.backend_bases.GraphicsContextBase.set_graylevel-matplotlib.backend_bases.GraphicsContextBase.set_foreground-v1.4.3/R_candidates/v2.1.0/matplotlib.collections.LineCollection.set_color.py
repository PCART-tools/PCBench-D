    def set_color(self, c):
        """
        Set the color(s) of the line collection.  *c* can be a
        matplotlib color arg (all patches have same color), or a
        sequence or rgba tuples; if it is a sequence the patches will
        cycle through the sequence.

        ACCEPTS: matplotlib color arg or sequence of rgba tuples
        """
        self.set_edgecolor(c)
        self.stale = True
