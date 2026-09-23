    def set_color(self, c):
        """
        Set the edgecolor.

        Parameters
        ----------
        c : color

        Notes
        -----
        This method does not modify the facecolor (which defaults to "none"),
        unlike the `.Patch.set_color` method defined in the parent class.  Use
        `.Patch.set_facecolor` to set the facecolor.
        """
        self.set_edgecolor(c)
        self.stale = True
