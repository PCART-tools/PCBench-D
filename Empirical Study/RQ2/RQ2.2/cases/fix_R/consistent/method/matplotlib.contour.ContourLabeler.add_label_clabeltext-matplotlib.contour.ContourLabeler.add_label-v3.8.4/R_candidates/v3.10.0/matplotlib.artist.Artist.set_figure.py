    def set_figure(self, fig):
        """
        Set the `.Figure` or `.SubFigure` instance the artist belongs to.

        Parameters
        ----------
        fig : `~matplotlib.figure.Figure` or `~matplotlib.figure.SubFigure`
        """
        # if this is a no-op just return
        if self._parent_figure is fig:
            return
        # if we currently have a figure (the case of both `self.figure`
        # and *fig* being none is taken care of above) we then user is
        # trying to change the figure an artist is associated with which
        # is not allowed for the same reason as adding the same instance
        # to more than one Axes
        if self._parent_figure is not None:
            raise RuntimeError("Can not put single artist in "
                               "more than one figure")
        self._parent_figure = fig
        if self._parent_figure and self._parent_figure is not self:
            self.pchanged()
        self.stale = True
