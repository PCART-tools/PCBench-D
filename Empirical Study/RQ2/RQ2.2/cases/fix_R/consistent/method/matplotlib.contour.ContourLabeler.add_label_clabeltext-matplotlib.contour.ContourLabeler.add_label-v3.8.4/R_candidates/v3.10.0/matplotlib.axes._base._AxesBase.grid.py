    @_docstring.interpd
    def grid(self, visible=None, which='major', axis='both', **kwargs):
        """
        Configure the grid lines.

        Parameters
        ----------
        visible : bool or None, optional
            Whether to show the grid lines.  If any *kwargs* are supplied, it
            is assumed you want the grid on and *visible* will be set to True.

            If *visible* is *None* and there are no *kwargs*, this toggles the
            visibility of the lines.

        which : {'major', 'minor', 'both'}, optional
            The grid lines to apply the changes on.

        axis : {'both', 'x', 'y'}, optional
            The axis to apply the changes on.

        **kwargs : `~matplotlib.lines.Line2D` properties
            Define the line properties of the grid, e.g.::

                grid(color='r', linestyle='-', linewidth=2)

            Valid keyword arguments are:

            %(Line2D:kwdoc)s

        Notes
        -----
        The axis is drawn as a unit, so the effective zorder for drawing the
        grid is determined by the zorder of each axis, not by the zorder of the
        `.Line2D` objects comprising the grid.  Therefore, to set grid zorder,
        use `.set_axisbelow` or, for more control, call the
        `~.Artist.set_zorder` method of each axis.
        """
        _api.check_in_list(['x', 'y', 'both'], axis=axis)
        if axis in ['x', 'both']:
            self.xaxis.grid(visible, which=which, **kwargs)
        if axis in ['y', 'both']:
            self.yaxis.grid(visible, which=which, **kwargs)
