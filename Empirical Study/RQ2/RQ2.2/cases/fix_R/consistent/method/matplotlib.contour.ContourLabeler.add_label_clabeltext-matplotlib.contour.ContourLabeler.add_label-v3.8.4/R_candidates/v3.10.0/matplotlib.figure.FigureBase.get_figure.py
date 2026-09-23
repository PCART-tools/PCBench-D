    def get_figure(self, root=None):
        """
        Return the `.Figure` or `.SubFigure` instance the (Sub)Figure belongs to.

        Parameters
        ----------
        root : bool, default=True
            If False, return the (Sub)Figure this artist is on.  If True,
            return the root Figure for a nested tree of SubFigures.

            .. deprecated:: 3.10

                From version 3.12 *root* will default to False.
        """
        if self._root_figure is self:
            # Top level Figure
            return self

        if self._parent is self._root_figure:
            # Return early to prevent the deprecation warning when *root* does not
            # matter
            return self._parent

        if root is None:
            # When deprecation expires, consider removing the docstring and just
            # inheriting the one from Artist.
            message = ('From Matplotlib 3.12 SubFigure.get_figure will by default '
                       'return the direct parent figure, which may be a SubFigure. '
                       'To suppress this warning, pass the root parameter.  Pass '
                       '`True` to maintain the old behavior and `False` to opt-in to '
                       'the future behavior.')
            _api.warn_deprecated('3.10', message=message)
            root = True

        if root:
            return self._root_figure

        return self._parent
