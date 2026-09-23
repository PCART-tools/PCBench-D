    def get_figure(self, root=False):
        """
        Return the `.Figure` or `.SubFigure` instance the artist belongs to.

        Parameters
        ----------
        root : bool, default=False
            If False, return the (Sub)Figure this artist is on.  If True,
            return the root Figure for a nested tree of SubFigures.
        """
        if root and self._parent_figure is not None:
            return self._parent_figure.get_figure(root=True)

        return self._parent_figure
