    @_docstring.interpd
    def axvline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a vertical line spanning the whole or fraction of the Axes.

        Note: If you want to set y-limits in data coordinates, use
        `~.Axes.vlines` instead.

        Parameters
        ----------
        x : float, default: 0
            y position in :ref:`data coordinates <coordinate-systems>`.

        ymin : float, default: 0
            The start y-position in :ref:`axes coordinates <coordinate-systems>`.
            Should be between 0 and 1, 0 being the bottom of the plot, 1 the
            top of the plot.

        ymax : float, default: 1
            The end y-position in :ref:`axes coordinates <coordinate-systems>`.
            Should be between 0 and 1, 0 being the bottom of the plot, 1 the
            top of the plot.

        Returns
        -------
        `~matplotlib.lines.Line2D`
            A `.Line2D` specified via two points ``(x, ymin)``, ``(x, ymax)``.
            Its transform is set such that *x* is in
            :ref:`data coordinates <coordinate-systems>` and *y* is in
            :ref:`axes coordinates <coordinate-systems>`.

            This is still a generic line and the vertical character is only
            realized through using identical *x* values for both points. Thus,
            if you want to change the *x* value later, you have to provide two
            values ``line.set_xdata([3, 3])``.

        Other Parameters
        ----------------
        **kwargs
            Valid keyword arguments are `.Line2D` properties, except for
            'transform':

            %(Line2D:kwdoc)s

        See Also
        --------
        vlines : Add vertical lines in data coordinates.
        axvspan : Add a vertical span (rectangle) across the axis.
        axline : Add a line with an arbitrary slope.

        Examples
        --------
        * draw a thick red vline at *x* = 0 that spans the yrange::

            >>> axvline(linewidth=4, color='r')

        * draw a default vline at *x* = 1 that spans the yrange::

            >>> axvline(x=1)

        * draw a default vline at *x* = .5 that spans the middle half of
          the yrange::

            >>> axvline(x=.5, ymin=0.25, ymax=0.75)
        """
        self._check_no_units([ymin, ymax], ['ymin', 'ymax'])
        if "transform" in kwargs:
            raise ValueError("'transform' is not allowed as a keyword "
                             "argument; axvline generates its own transform.")
        xmin, xmax = self.get_xbound()

        # Strip away the units for comparison with non-unitized bounds.
        xx, = self._process_unit_info([("x", x)], kwargs)
        scalex = (xx < xmin) or (xx > xmax)

        trans = self.get_xaxis_transform(which='grid')
        l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
        self.add_line(l)
        l.get_path()._interpolation_steps = mpl.axis.GRIDLINE_INTERPOLATION_STEPS
        if scalex:
            self._request_autoscale_view("x")
        return l
