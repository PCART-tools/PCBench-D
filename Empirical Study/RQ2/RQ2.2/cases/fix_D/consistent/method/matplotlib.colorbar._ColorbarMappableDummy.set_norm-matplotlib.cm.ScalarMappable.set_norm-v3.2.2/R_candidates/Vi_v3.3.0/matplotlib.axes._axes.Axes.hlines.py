    @_preprocess_data(replace_names=["y", "xmin", "xmax", "colors"],
                      label_namer="y")
    def hlines(self, y, xmin, xmax, colors=None, linestyles='solid',
               label='', **kwargs):
        """
        Plot horizontal lines at each *y* from *xmin* to *xmax*.

        Parameters
        ----------
        y : float or array-like
            y-indexes where to plot the lines.

        xmin, xmax : float or array-like
            Respective beginning and end of each line. If scalars are
            provided, all lines will have same length.

        colors : list of colors, default: :rc:`lines.color`

        linestyles : {'solid', 'dashed', 'dashdot', 'dotted'}, optional

        label : str, default: ''

        Returns
        -------
        `~matplotlib.collections.LineCollection`

        Other Parameters
        ----------------
        **kwargs :  `~matplotlib.collections.LineCollection` properties.

        See Also
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

        # Create and combine masked_arrays from input
        y, xmin, xmax = cbook._combine_masks(y, xmin, xmax)
        y = np.ravel(y)
        xmin = np.ravel(xmin)
        xmax = np.ravel(xmax)

        masked_verts = np.ma.empty((len(y), 2, 2))
        masked_verts[:, 0, 0] = xmin
        masked_verts[:, 0, 1] = y
        masked_verts[:, 1, 0] = xmax
        masked_verts[:, 1, 1] = y

        lines = mcoll.LineCollection(masked_verts, colors=colors,
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
            self._request_autoscale_view()

        return lines
