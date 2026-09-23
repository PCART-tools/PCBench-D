    @docstring.dedent_interpd
    def axvline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a vertical line across the axes.

        Parameters
        ----------
        x : scalar, optional, default: 0
            x position in data coordinates of the vertical line.

        ymin : scalar, optional, default: 0
            Should be between 0 and 1, 0 being the bottom of the plot, 1 the
            top of the plot.

        ymax : scalar, optional, default: 1
            Should be between 0 and 1, 0 being the bottom of the plot, 1 the
            top of the plot.

        Returns
        -------
        :class:`~matplotlib.lines.Line2D`

        Other Parameters
        ----------------
        **kwargs :
            Valid kwargs are :class:`~matplotlib.lines.Line2D` properties,
            with the exception of 'transform':

            %(Line2D)s

        Examples
        --------
        * draw a thick red vline at *x* = 0 that spans the yrange::

            >>> axvline(linewidth=4, color='r')

        * draw a default vline at *x* = 1 that spans the yrange::

            >>> axvline(x=1)

        * draw a default vline at *x* = .5 that spans the middle half of
          the yrange::

            >>> axvline(x=.5, ymin=0.25, ymax=0.75)

        See also
        --------
        vlines : add vertical lines in data coordinates
        axvspan : add a vertical span (rectangle) across the axis
        """

        if "transform" in kwargs:
            raise ValueError(
                "'transform' is not allowed as a kwarg;"
                + "axvline generates its own transform.")
        xmin, xmax = self.get_xbound()

        # We need to strip away the units for comparison with
        # non-unitized bounds
        self._process_unit_info(xdata=x, kwargs=kwargs)
        xx = self.convert_xunits(x)
        scalex = (xx < xmin) or (xx > xmax)

        trans = self.get_xaxis_transform(which='grid')
        l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
        self.add_line(l)
        self.autoscale_view(scalex=scalex, scaley=False)
        return l
