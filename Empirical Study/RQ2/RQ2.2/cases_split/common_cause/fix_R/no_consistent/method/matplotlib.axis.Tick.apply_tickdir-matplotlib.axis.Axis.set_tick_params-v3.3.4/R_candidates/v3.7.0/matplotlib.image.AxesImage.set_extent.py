    def set_extent(self, extent, **kwargs):
        """
        Set the image extent.

        Parameters
        ----------
        extent : 4-tuple of float
            The position and size of the image as tuple
            ``(left, right, bottom, top)`` in data coordinates.
        **kwargs
            Other parameters from which unit info (i.e., the *xunits*,
            *yunits*, *zunits* (for 3D axes), *runits* and *thetaunits* (for
            polar axes) entries are applied, if present.

        Notes
        -----
        This updates ``ax.dataLim``, and, if autoscaling, sets ``ax.viewLim``
        to tightly fit the image, regardless of ``dataLim``.  Autoscaling
        state is not changed, so following this with ``ax.autoscale_view()``
        will redo the autoscaling in accord with ``dataLim``.
        """
        (xmin, xmax), (ymin, ymax) = self.axes._process_unit_info(
            [("x", [extent[0], extent[1]]),
             ("y", [extent[2], extent[3]])],
            kwargs)
        if kwargs:
            raise _api.kwarg_error("set_extent", kwargs)
        xmin = self.axes._validate_converted_limits(
            xmin, self.convert_xunits)
        xmax = self.axes._validate_converted_limits(
            xmax, self.convert_xunits)
        ymin = self.axes._validate_converted_limits(
            ymin, self.convert_yunits)
        ymax = self.axes._validate_converted_limits(
            ymax, self.convert_yunits)
        extent = [xmin, xmax, ymin, ymax]

        self._extent = extent
        corners = (xmin, ymin), (xmax, ymax)
        self.axes.update_datalim(corners)
        self.sticky_edges.x[:] = [xmin, xmax]
        self.sticky_edges.y[:] = [ymin, ymax]
        if self.axes.get_autoscalex_on():
            self.axes.set_xlim((xmin, xmax), auto=None)
        if self.axes.get_autoscaley_on():
            self.axes.set_ylim((ymin, ymax), auto=None)
        self.stale = True
