    @_docstring.interpd
    def axhspan(self, ymin, ymax, xmin=0, xmax=1, **kwargs):
        """
        Add a horizontal span (rectangle) across the Axes.

        The rectangle spans from *ymin* to *ymax* vertically, and, by default,
        the whole x-axis horizontally.  The x-span can be set using *xmin*
        (default: 0) and *xmax* (default: 1) which are in axis units; e.g.
        ``xmin = 0.5`` always refers to the middle of the x-axis regardless of
        the limits set by `~.Axes.set_xlim`.

        Parameters
        ----------
        ymin : float
            Lower y-coordinate of the span, in data units.
        ymax : float
            Upper y-coordinate of the span, in data units.
        xmin : float, default: 0
            Lower x-coordinate of the span, in x-axis (0-1) units.
        xmax : float, default: 1
            Upper x-coordinate of the span, in x-axis (0-1) units.

        Returns
        -------
        `~matplotlib.patches.Rectangle`
            Horizontal span (rectangle) from (xmin, ymin) to (xmax, ymax).

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Rectangle` properties

        %(Rectangle:kwdoc)s

        See Also
        --------
        axvspan : Add a vertical span across the Axes.
        """
        # Strip units away.
        self._check_no_units([xmin, xmax], ['xmin', 'xmax'])
        (ymin, ymax), = self._process_unit_info([("y", [ymin, ymax])], kwargs)

        p = mpatches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, **kwargs)
        p.set_transform(self.get_yaxis_transform(which="grid"))
        # For Rectangles and non-separable transforms, add_patch can be buggy
        # and update the x limits even though it shouldn't do so for an
        # yaxis_transformed patch, so undo that update.
        ix = self.dataLim.intervalx.copy()
        mx = self.dataLim.minposx
        self.add_patch(p)
        self.dataLim.intervalx = ix
        self.dataLim.minposx = mx
        p.get_path()._interpolation_steps = mpl.axis.GRIDLINE_INTERPOLATION_STEPS
        self._request_autoscale_view("y")
        return p
