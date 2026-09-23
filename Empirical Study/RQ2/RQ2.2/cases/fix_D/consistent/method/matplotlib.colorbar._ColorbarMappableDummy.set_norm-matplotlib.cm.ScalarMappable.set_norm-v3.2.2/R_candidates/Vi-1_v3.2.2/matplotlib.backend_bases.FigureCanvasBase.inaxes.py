    def inaxes(self, xy):
        """
        Return the topmost visible `~.axes.Axes` containing the point *xy*.

        Parameters
        ----------
        xy : tuple or list
            (x, y) coordinates.
            x position - pixels from left of canvas.
            y position - pixels from bottom of canvas.

        Returns
        -------
        axes : `~matplotlib.axes.Axes` or None
            The topmost visible axes containing the point, or None if no axes.
        """
        axes_list = [a for a in self.figure.get_axes()
                     if a.patch.contains_point(xy) and a.get_visible()]
        if axes_list:
            axes = cbook._topmost_artist(axes_list)
        else:
            axes = None

        return axes
