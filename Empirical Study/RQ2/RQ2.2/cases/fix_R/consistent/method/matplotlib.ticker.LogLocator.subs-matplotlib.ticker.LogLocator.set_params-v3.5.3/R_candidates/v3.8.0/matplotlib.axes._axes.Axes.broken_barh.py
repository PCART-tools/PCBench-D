    @_preprocess_data()
    @_docstring.dedent_interpd
    def broken_barh(self, xranges, yrange, **kwargs):
        """
        Plot a horizontal sequence of rectangles.

        A rectangle is drawn for each element of *xranges*. All rectangles
        have the same vertical position and size defined by *yrange*.

        Parameters
        ----------
        xranges : sequence of tuples (*xmin*, *xwidth*)
            The x-positions and extents of the rectangles. For each tuple
            (*xmin*, *xwidth*) a rectangle is drawn from *xmin* to *xmin* +
            *xwidth*.
        yrange : (*ymin*, *yheight*)
            The y-position and extent for all the rectangles.

        Returns
        -------
        `~.collections.PolyCollection`

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        **kwargs : `.PolyCollection` properties

            Each *kwarg* can be either a single argument applying to all
            rectangles, e.g.::

                facecolors='black'

            or a sequence of arguments over which is cycled, e.g.::

                facecolors=('black', 'blue')

            would create interleaving black and blue rectangles.

            Supported keywords:

            %(PolyCollection:kwdoc)s
        """
        # process the unit information
        xdata = cbook._safe_first_finite(xranges) if len(xranges) else None
        ydata = cbook._safe_first_finite(yrange) if len(yrange) else None
        self._process_unit_info(
            [("x", xdata), ("y", ydata)], kwargs, convert=False)

        vertices = []
        y0, dy = yrange
        y0, y1 = self.convert_yunits((y0, y0 + dy))
        for xr in xranges:  # convert the absolute values, not the x and dx
            try:
                x0, dx = xr
            except Exception:
                raise ValueError(
                    "each range in xrange must be a sequence with two "
                    "elements (i.e. xrange must be an (N, 2) array)") from None
            x0, x1 = self.convert_xunits((x0, x0 + dx))
            vertices.append([(x0, y0), (x0, y1), (x1, y1), (x1, y0)])

        col = mcoll.PolyCollection(np.array(vertices), **kwargs)
        self.add_collection(col, autolim=True)
        self._request_autoscale_view()

        return col
