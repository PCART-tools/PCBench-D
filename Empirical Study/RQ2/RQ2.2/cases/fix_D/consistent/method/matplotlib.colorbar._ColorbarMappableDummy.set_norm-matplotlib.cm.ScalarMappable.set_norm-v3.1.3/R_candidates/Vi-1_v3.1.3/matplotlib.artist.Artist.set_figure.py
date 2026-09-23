    def set_figure(self, fig):
        """
        Set the `.Figure` instance the artist belongs to.

        Parameters
        ----------
        fig : `.Figure`
        """
        # if this is a no-op just return
        if self.figure is fig:
            return
        # if we currently have a figure (the case of both `self.figure`
        # and `fig` being none is taken care of above) we then user is
        # trying to change the figure an artist is associated with which
        # is not allowed for the same reason as adding the same instance
        # to more than one Axes
        if self.figure is not None:
            raise RuntimeError("Can not put single artist in "
                               "more than one figure")
        self.figure = fig
        if self.figure and self.figure is not self:
            self.pchanged()
        self.stale = True
