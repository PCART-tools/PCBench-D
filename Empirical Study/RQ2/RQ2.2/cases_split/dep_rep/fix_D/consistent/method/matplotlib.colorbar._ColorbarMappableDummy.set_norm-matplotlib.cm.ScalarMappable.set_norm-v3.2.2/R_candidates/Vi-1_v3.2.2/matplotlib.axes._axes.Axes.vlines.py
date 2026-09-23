    @_preprocess_data(replace_names=["x", "ymin", "ymax", "colors"],
                      label_namer="x")
    def vlines(self, x, ymin, ymax, colors='k', linestyles='solid',
               label='', **kwargs):
        """
        Plot vertical lines.

        Plot vertical lines at each *x* from *ymin* to *ymax*.

        Parameters
        ----------
        x : scalar or 1D array-like
            x-indexes where to plot the lines.

        ymin, ymax : scalar or 1D array-like
            Respective beginning and end of each line. If scalars are
            provided, all lines will have same length.

        colors : array-like of colors, optional, default: 'k'

        linestyles : {'solid', 'dashed', 'dashdot', 'dotted'}, optional

        label : str, optional, default: ''

        Returns
        -------
        lines : `~matplotlib.collections.LineCollection`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.collections.LineCollection` properties.

        See also
        --------
        hlines : horizontal lines
        axvline: vertical line across the axes
        """

        self._process_unit_info(xdata=x, ydata=[ymin, ymax], kwargs=kwargs)

        # We do the conversion first since not all unitized data is uniform
        x = self.convert_xunits(x)
        ymin = self.convert_yunits(ymin)
        ymax = self.convert_yunits(ymax)

        if not np.iterable(x):
            x = [x]
        if not np.iterable(ymin):
            ymin = [ymin]
        if not np.iterable(ymax):
            ymax = [ymax]

        x, ymin, ymax = cbook.delete_masked_points(x, ymin, ymax)

        x = np.ravel(x)
        ymin = np.resize(ymin, x.shape)
        ymax = np.resize(ymax, x.shape)

        verts = [((thisx, thisymin), (thisx, thisymax))
                 for thisx, thisymin, thisymax in zip(x, ymin, ymax)]
        lines = mcoll.LineCollection(verts, colors=colors,
                                     linestyles=linestyles, label=label)
        self.add_collection(lines, autolim=False)
        lines.update(kwargs)

        if len(x) > 0:
            minx = x.min()
            maxx = x.max()
            miny = min(ymin.min(), ymax.min())
            maxy = max(ymin.max(), ymax.max())

            corners = (minx, miny), (maxx, maxy)
            self.update_datalim(corners)
            self._request_autoscale_view()

        return lines
