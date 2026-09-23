    @docstring.dedent_interpd
    def axline(self, xy1, xy2=None, *, slope=None, **kwargs):
        """
        Add an infinitely long straight line.

        The line can be defined either by two points *xy1* and *xy2*, or
        by one point *xy1* and a *slope*.

        This draws a straight line "on the screen", regardless of the x and y
        scales, and is thus also suitable for drawing exponential decays in
        semilog plots, power laws in loglog plots, etc. However, *slope*
        should only be used with linear scales; It has no clear meaning for
        all other scales, and thus the behavior is undefined. Please specify
        the line using the points *xy1*, *xy2* for non-linear scales.

        Parameters
        ----------
        xy1, xy2 : (float, float)
            Points for the line to pass through.
            Either *xy2* or *slope* has to be given.
        slope : float, optional
            The slope of the line. Either *xy2* or *slope* has to be given.

        Returns
        -------
        `.Line2D`

        Other Parameters
        ----------------
        **kwargs
            Valid kwargs are `.Line2D` properties, with the exception of
            'transform':

            %(_Line2D_docstr)s

        See Also
        --------
        axhline : for horizontal lines
        axvline : for vertical lines

        Examples
        --------
        Draw a thick red line passing through (0, 0) and (1, 1)::

            >>> axline((0, 0), (1, 1), linewidth=4, color='r')
        """
        def _to_points(xy1, xy2, slope):
            """
            Check for a valid combination of input parameters and convert
            to two points, if necessary.
            """
            if (xy2 is None and slope is None or
                    xy2 is not None and slope is not None):
                raise TypeError(
                    "Exactly one of 'xy2' and 'slope' must be given")
            if xy2 is None:
                x1, y1 = xy1
                xy2 = (x1, y1 + 1) if np.isinf(slope) else (x1 + 1, y1 + slope)
            return xy1, xy2

        if "transform" in kwargs:
            raise TypeError("'transform' is not allowed as a kwarg; "
                            "axline generates its own transform")
        if slope is not None and (self.get_xscale() != 'linear' or
                                  self.get_yscale() != 'linear'):
            raise TypeError("'slope' cannot be used with non-linear scales")

        datalim = [xy1] if xy2 is None else [xy1, xy2]
        (x1, y1), (x2, y2) = _to_points(xy1, xy2, slope)
        line = mlines._AxLine([x1, x2], [y1, y2], **kwargs)
        # Like add_line, but correctly handling data limits.
        self._set_artist_props(line)
        if line.get_clip_path() is None:
            line.set_clip_path(self.patch)
        if not line.get_label():
            line.set_label(f"_line{len(self.lines)}")
        self.lines.append(line)
        line._remove_method = self.lines.remove
        self.update_datalim(datalim)

        self._request_autoscale_view()
        return line
