    @_preprocess_data(replace_names=["y", "xmin", "xmax", "colors"],
                      label_namer="y")
    def hlines(self, y, xmin, xmax, colors='k', linestyles='solid',
               label='', **kwargs):
        """
        Plot horizontal lines at each *y* from *xmin* to *xmax*.

        Parameters
        ----------
        y : scalar or sequence of scalar
            y-indexes where to plot the lines.

        xmin, xmax : scalar or 1D array_like
            Respective beginning and end of each line. If scalars are
            provided, all lines will have same length.

        colors : array_like of colors, optional, default: 'k'

        linestyles : {'solid', 'dashed', 'dashdot', 'dotted'}, optional

        label : string, optional, default: ''

        Returns
        -------
        lines : `~matplotlib.collections.LineCollection`

        Other Parameters
        ----------------
        **kwargs :  `~matplotlib.collections.LineCollection` properties.

        See also
        --------
        vlines : vertical lines
        axhline: horizontal line across the axes
        """

        # We do the conversion first since not all unitized data is uniform
        # process the unit information
        self._process_unit_info([xmin, xmax], y, kwargs=kwargs)
        y = self.convert_yunits(y)
        xmin = self.convert_xunits(xmin)
        xmax = self.convert_xunits(xmax)

        if not np.iterable(y):
            y = [y]
        if not np.iterable(xmin):
            xmin = [xmin]
        if not np.iterable(xmax):
            xmax = [xmax]

        y, xmin, xmax = cbook.delete_masked_points(y, xmin, xmax)

        y = np.ravel(y)
        xmin = np.resize(xmin, y.shape)
        xmax = np.resize(xmax, y.shape)

        verts = [((thisxmin, thisy), (thisxmax, thisy))
                 for thisxmin, thisxmax, thisy in zip(xmin, xmax, y)]
        lines = mcoll.LineCollection(verts, colors=colors,
                                     linestyles=linestyles, label=label)
        self.add_collection(lines, autolim=False)
        lines.update(kwargs)

        if len(y) > 0:
            minx = min(xmin.min(), xmax.min())
            maxx = max(xmin.max(), xmax.max())
            miny = y.min()
            maxy = y.max()

            corners = (minx, miny), (maxx, maxy)

            self.update_datalim(corners)
            self.autoscale_view()

        return lines
