    @docstring.dedent_interpd
    def grid(self, b=None, which='major', axis='both', **kwargs):
        """
        Configure the grid lines.

        Parameters
        ----------
        b : bool or None
            Whether to show the grid lines. If any *kwargs* are supplied,
            it is assumed you want the grid on and *b* will be set to True.

            If *b* is *None* and there are no *kwargs*, this toggles the
            visibility of the lines.

        which : {'major', 'minor', 'both'}
            The grid lines to apply the changes on.

        axis : {'both', 'x', 'y'}
            The axis to apply the changes on.

        **kwargs : `.Line2D` properties
            Define the line properties of the grid, e.g.::

                grid(color='r', linestyle='-', linewidth=2)

            Valid *kwargs* are

            %(Line2D)s

        Notes
        -----
        The grid will be drawn according to the axes' zorder and not its own.
        """
        if len(kwargs):
            b = True
        elif b is not None:
            b = _string_to_bool(b)

        if axis == 'x' or axis == 'both':
            self.xaxis.grid(b, which=which, **kwargs)
        if axis == 'y' or axis == 'both':
            self.yaxis.grid(b, which=which, **kwargs)
