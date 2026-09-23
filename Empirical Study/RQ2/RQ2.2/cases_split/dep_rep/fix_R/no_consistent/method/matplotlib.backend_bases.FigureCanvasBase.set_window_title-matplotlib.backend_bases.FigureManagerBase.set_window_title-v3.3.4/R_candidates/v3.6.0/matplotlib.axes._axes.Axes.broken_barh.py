    @_preprocess_data()
    @_docstring.dedent_interpd
    def broken_barh(self, xranges, yrange, **kwargs):
        """
        Plot a horizontal sequence of rectangles.

        A rectangle is drawn for each element of *xranges*. All rectangles
        have the same vertical position and size defined by *yrange*.

        This is a convenience function for instantiating a
        `.BrokenBarHCollection`, adding it to the Axes and autoscaling the
        view.

        Parameters
        ----------
        xranges : sequence of tuples (*xmin*, *xwidth*)
            The x-positions and extends of the rectangles. For each tuple
            (*xmin*, *xwidth*) a rectangle is drawn from *xmin* to *xmin* +
            *xwidth*.
        yrange : (*ymin*, *yheight*)
            The y-position and extend for all the rectangles.

        Returns
        -------
        `~.collections.BrokenBarHCollection`

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        **kwargs : `.BrokenBarHCollection` properties

            Each *kwarg* can be either a single argument applying to all
            rectangles, e.g.::

                facecolors='black'

            or a sequence of arguments over which is cycled, e.g.::

                facecolors=('black', 'blue')

            would create interleaving black and blue rectangles.

            Supported keywords:

            %(BrokenBarHCollection:kwdoc)s
        """
        # process the unit information
        if len(xranges):
            xdata = cbook._safe_first_non_none(xranges)
        else:
            xdata = None
        if len(yrange):
            ydata = cbook._safe_first_non_none(yrange)
        else:
            ydata = None
        self._process_unit_info(
            [("x", xdata), ("y", ydata)], kwargs, convert=False)
        xranges_conv = []
        for xr in xranges:
            if len(xr) != 2:
                raise ValueError('each range in xrange must be a sequence '
                                 'with two elements (i.e. an Nx2 array)')
            # convert the absolute values, not the x and dx...
            x_conv = np.asarray(self.convert_xunits(xr[0]))
            x1 = self._convert_dx(xr[1], xr[0], x_conv, self.convert_xunits)
            xranges_conv.append((x_conv, x1))

        yrange_conv = self.convert_yunits(yrange)

        col = mcoll.BrokenBarHCollection(xranges_conv, yrange_conv, **kwargs)
        self.add_collection(col, autolim=True)
        self._request_autoscale_view()

        return col
