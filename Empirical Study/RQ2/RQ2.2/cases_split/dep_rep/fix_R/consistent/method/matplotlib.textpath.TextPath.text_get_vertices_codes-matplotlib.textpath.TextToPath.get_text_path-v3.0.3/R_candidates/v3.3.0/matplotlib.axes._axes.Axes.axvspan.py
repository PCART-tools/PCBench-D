    def axvspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        """
        Add a vertical span (rectangle) across the axes.

        The rectangle spans from *xmin* to *xmax* horizontally, and, by
        default, the whole y-axis vertically.  The y-span can be set using
        *ymin* (default: 0) and *ymax* (default: 1) which are in axis units;
        e.g. ``ymin = 0.5`` always refers to the middle of the y-axis
        regardless of the limits set by `~.Axes.set_ylim`.

        Parameters
        ----------
        xmin : float
            Lower x-coordinate of the span, in data units.
        xmax : float
            Upper x-coordinate of the span, in data units.
        ymin : float, default: 0
            Lower y-coordinate of the span, in y-axis units (0-1).
        ymax : float, default: 1
            Upper y-coordinate of the span, in y-axis units (0-1).

        Returns
        -------
        `~matplotlib.patches.Polygon`
            Vertical span (rectangle) from (xmin, ymin) to (xmax, ymax).

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Polygon` properties

        %(Polygon)s

        See Also
        --------
        axhspan : Add a horizontal span across the axes.

        Examples
        --------
        Draw a vertical, green, translucent rectangle from x = 1.25 to
        x = 1.55 that spans the yrange of the axes.

        >>> axvspan(1.25, 1.55, facecolor='g', alpha=0.5)

        """
        trans = self.get_xaxis_transform(which='grid')

        # process the unit information
        self._process_unit_info([xmin, xmax], [ymin, ymax], kwargs=kwargs)

        # first we need to strip away the units
        xmin, xmax = self.convert_xunits([xmin, xmax])
        ymin, ymax = self.convert_yunits([ymin, ymax])

        verts = [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)]
        p = mpatches.Polygon(verts, **kwargs)
        p.set_transform(trans)
        self.add_patch(p)
        self._request_autoscale_view(scaley=False)
        return p
