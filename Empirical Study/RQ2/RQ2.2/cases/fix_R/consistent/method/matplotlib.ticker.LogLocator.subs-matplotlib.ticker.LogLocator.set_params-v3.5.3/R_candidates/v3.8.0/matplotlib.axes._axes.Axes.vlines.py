    @_preprocess_data(replace_names=["x", "ymin", "ymax", "colors"],
                      label_namer="x")
    def vlines(self, x, ymin, ymax, colors=None, linestyles='solid',
               label='', **kwargs):
        """
        Plot vertical lines at each *x* from *ymin* to *ymax*.

        Parameters
        ----------
        x : float or array-like
            x-indexes where to plot the lines.

        ymin, ymax : float or array-like
            Respective beginning and end of each line. If scalars are
            provided, all lines will have the same length.

        colors : color or list of colors, default: :rc:`lines.color`

        linestyles : {'solid', 'dashed', 'dashdot', 'dotted'}, default: 'solid'

        label : str, default: ''

        Returns
        -------
        `~matplotlib.collections.LineCollection`

        Other Parameters
        ----------------
        data : indexable object, optional
            DATA_PARAMETER_PLACEHOLDER
        **kwargs : `~matplotlib.collections.LineCollection` properties.

        See Also
        --------
        hlines : horizontal lines
        axvline : vertical line across the Axes
        """

        # We do the conversion first since not all unitized data is uniform
        x, ymin, ymax = self._process_unit_info(
            [("x", x), ("y", ymin), ("y", ymax)], kwargs)

        if not np.iterable(x):
            x = [x]
        if not np.iterable(ymin):
            ymin = [ymin]
        if not np.iterable(ymax):
            ymax = [ymax]

        # Create and combine masked_arrays from input
        x, ymin, ymax = cbook._combine_masks(x, ymin, ymax)
        x = np.ravel(x)
        ymin = np.ravel(ymin)
        ymax = np.ravel(ymax)

        masked_verts = np.ma.empty((len(x), 2, 2))
        masked_verts[:, 0, 0] = x
        masked_verts[:, 0, 1] = ymin
        masked_verts[:, 1, 0] = x
        masked_verts[:, 1, 1] = ymax

        lines = mcoll.LineCollection(masked_verts, colors=colors,
                                     linestyles=linestyles, label=label)
        self.add_collection(lines, autolim=False)
        lines._internal_update(kwargs)

        if len(x) > 0:
            # Extreme values of x/ymin/ymax.  Using masked_verts here handles
            # the case of x being a masked *object* array (as can be generated
            # e.g. by errorbar()), which would make nanmin/nanmax stumble.
            updatex = True
            updatey = True
            if self.name == "rectilinear":
                datalim = lines.get_datalim(self.transData)
                t = lines.get_transform()
                updatex, updatey = t.contains_branch_seperately(self.transData)
                minx = np.nanmin(datalim.xmin)
                maxx = np.nanmax(datalim.xmax)
                miny = np.nanmin(datalim.ymin)
                maxy = np.nanmax(datalim.ymax)
            else:
                minx = np.nanmin(masked_verts[..., 0])
                maxx = np.nanmax(masked_verts[..., 0])
                miny = np.nanmin(masked_verts[..., 1])
                maxy = np.nanmax(masked_verts[..., 1])

            corners = (minx, miny), (maxx, maxy)
            self.update_datalim(corners, updatex, updatey)
            self._request_autoscale_view()
        return lines
