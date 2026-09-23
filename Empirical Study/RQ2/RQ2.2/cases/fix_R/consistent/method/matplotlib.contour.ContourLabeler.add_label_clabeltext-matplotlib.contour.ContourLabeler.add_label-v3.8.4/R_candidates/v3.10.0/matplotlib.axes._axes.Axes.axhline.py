    @_docstring.interpd
    def axhline(self, y=0, xmin=0, xmax=1, **kwargs):
        """
        Add a horizontal line spanning the whole or fraction of the Axes.

        Note: If you want to set x-limits in data coordinates, use
        `~.Axes.hlines` instead.

        Parameters
        ----------
        y : float, default: 0
            y position in :ref:`data coordinates <coordinate-systems>`.

        xmin : float, default: 0
            The start x-position in :ref:`axes coordinates <coordinate-systems>`.
            Should be between 0 and 1, 0 being the far left of the plot,
            1 the far right of the plot.

        xmax : float, default: 1
            The end x-position in :ref:`axes coordinates <coordinate-systems>`.
            Should be between 0 and 1, 0 being the far left of the plot,
            1 the far right of the plot.

        Returns
        -------
        `~matplotlib.lines.Line2D`
            A `.Line2D` specified via two points ``(xmin, y)``, ``(xmax, y)``.
            Its transform is set such that *x* is in
            :ref:`axes coordinates <coordinate-systems>` and *y* is in
            :ref:`data coordinates <coordinate-systems>`.

            This is still a generic line and the horizontal character is only
            realized through using identical *y* values for both points. Thus,
            if you want to change the *y* value later, you have to provide two
            values ``line.set_ydata([3, 3])``.

        Other Parameters
        ----------------
        **kwargs
            Valid keyword arguments are `.Line2D` properties, except for
            'transform':

            %(Line2D:kwdoc)s

        See Also
        --------
        hlines : Add horizontal lines in data coordinates.
        axhspan : Add a horizontal span (rectangle) across the axis.
        axline : Add a line with an arbitrary slope.

        Examples
        --------
        * draw a thick red hline at 'y' = 0 that spans the xrange::

            >>> axhline(linewidth=4, color='r')

        * draw a default hline at 'y' = 1 that spans the xrange::

            >>> axhline(y=1)

        * draw a default hline at 'y' = .5 that spans the middle half of
          the xrange::

            >>> axhline(y=.5, xmin=0.25, xmax=0.75)
        """
        self._check_no_units([xmin, xmax], ['xmin', 'xmax'])
        if "transform" in kwargs:
            raise ValueError("'transform' is not allowed as a keyword "
                             "argument; axhline generates its own transform.")
        ymin, ymax = self.get_ybound()

        # Strip away the units for comparison with non-unitized bounds.
        yy, = self._process_unit_info([("y", y)], kwargs)
        scaley = (yy < ymin) or (yy > ymax)

        trans = self.get_yaxis_transform(which='grid')
        l = mlines.Line2D([xmin, xmax], [y, y], transform=trans, **kwargs)
        self.add_line(l)
        l.get_path()._interpolation_steps = mpl.axis.GRIDLINE_INTERPOLATION_STEPS
        if scaley:
            self._request_autoscale_view("y")
        return l
