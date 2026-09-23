    @docstring.dedent_interpd
    def grid(self, b=None, which='major', axis='both', **kwargs):
        """
        Turn the axes grids on or off.

        Set the axes grids on or off; *b* is a boolean.  (For MATLAB
        compatibility, *b* may also be a string, 'on' or 'off'.)

        If *b* is *None* and ``len(kwargs)==0``, toggle the grid state.  If
        *kwargs* are supplied, it is assumed that you want a grid and *b*
        is thus set to *True*.

        *which* can be 'major' (default), 'minor', or 'both' to control
        whether major tick grids, minor tick grids, or both are affected.

        *axis* can be 'both' (default), 'x', or 'y' to control which
        set of gridlines are drawn.

        *kwargs* are used to set the grid line properties, e.g.,::

           ax.grid(color='r', linestyle='-', linewidth=2)

        Valid :class:`~matplotlib.lines.Line2D` kwargs are

        %(Line2D)s

        """
        if len(kwargs):
            b = True
        elif b is not None:
            b = _string_to_bool(b)

        if axis == 'x' or axis == 'both':
            self.xaxis.grid(b, which=which, **kwargs)
        if axis == 'y' or axis == 'both':
            self.yaxis.grid(b, which=which, **kwargs)
