    def apply_aspect(self, position=None):
        """
        Adjust the Axes for a specified data aspect ratio.

        Depending on `.get_adjustable` this will modify either the
        Axes box (position) or the view limits. In the former case,
        `~matplotlib.axes.Axes.get_anchor` will affect the position.

        Parameters
        ----------
        position : None or .Bbox

            .. note::
                This parameter exists for historic reasons and is considered
                internal. End users should not use it.

            If not ``None``, this defines the position of the
            Axes within the figure as a Bbox. See `~.Axes.get_position`
            for further details.

        Notes
        -----
        This is called automatically when each Axes is drawn.  You may need
        to call it yourself if you need to update the Axes position and/or
        view limits before the Figure is drawn.

        An alternative with a broader scope is `.Figure.draw_without_rendering`,
        which updates all stale components of a figure, not only the positioning /
        view limits of a single Axes.

        See Also
        --------
        matplotlib.axes.Axes.set_aspect
            For a description of aspect ratio handling.
        matplotlib.axes.Axes.set_adjustable
            Set how the Axes adjusts to achieve the required aspect ratio.
        matplotlib.axes.Axes.set_anchor
            Set the position in case of extra space.
        matplotlib.figure.Figure.draw_without_rendering
            Update all stale components of a figure.

        Examples
        --------
        A typical usage example would be the following. `~.Axes.imshow` sets the
        aspect to 1, but adapting the Axes position and extent to reflect this is
        deferred until rendering for performance reasons. If you want to know the
        Axes size before, you need to call `.apply_aspect` to get the correct
        values.

        >>> fig, ax = plt.subplots()
        >>> ax.imshow(np.zeros((3, 3)))
        >>> ax.bbox.width, ax.bbox.height
        (496.0, 369.59999999999997)
        >>> ax.apply_aspect()
        >>> ax.bbox.width, ax.bbox.height
        (369.59999999999997, 369.59999999999997)
        """
        if position is None:
            position = self.get_position(original=True)

        aspect = self.get_aspect()

        if aspect == 'auto' and self._box_aspect is None:
            self._set_position(position, which='active')
            return

        trans = self.get_figure(root=False).transSubfigure
        bb = mtransforms.Bbox.unit().transformed(trans)
        # this is the physical aspect of the panel (or figure):
        fig_aspect = bb.height / bb.width

        if self._adjustable == 'box':
            if self in self._twinned_axes:
                raise RuntimeError("Adjustable 'box' is not allowed in a "
                                   "twinned Axes; use 'datalim' instead")
            box_aspect = aspect * self.get_data_ratio()
            pb = position.frozen()
            pb1 = pb.shrunk_to_aspect(box_aspect, pb, fig_aspect)
            self._set_position(pb1.anchored(self.get_anchor(), pb), 'active')
            return

        # The following is only seen if self._adjustable == 'datalim'
        if self._box_aspect is not None:
            pb = position.frozen()
            pb1 = pb.shrunk_to_aspect(self._box_aspect, pb, fig_aspect)
            self._set_position(pb1.anchored(self.get_anchor(), pb), 'active')
            if aspect == "auto":
                return

        # reset active to original in case it had been changed by prior use
        # of 'box'
        if self._box_aspect is None:
            self._set_position(position, which='active')
        else:
            position = pb1.anchored(self.get_anchor(), pb)

        x_trf = self.xaxis.get_transform()
        y_trf = self.yaxis.get_transform()
        xmin, xmax = x_trf.transform(self.get_xbound())
        ymin, ymax = y_trf.transform(self.get_ybound())
        xsize = max(abs(xmax - xmin), 1e-30)
        ysize = max(abs(ymax - ymin), 1e-30)

        box_aspect = fig_aspect * (position.height / position.width)
        data_ratio = box_aspect / aspect

        y_expander = data_ratio * xsize / ysize - 1
        # If y_expander > 0, the dy/dx viewLim ratio needs to increase
        if abs(y_expander) < 0.005:
            return

        dL = self.dataLim
        x0, x1 = x_trf.transform(dL.intervalx)
        y0, y1 = y_trf.transform(dL.intervaly)
        xr = 1.05 * (x1 - x0)
        yr = 1.05 * (y1 - y0)

        xmarg = xsize - xr
        ymarg = ysize - yr
        Ysize = data_ratio * xsize
        Xsize = ysize / data_ratio
        Xmarg = Xsize - xr
        Ymarg = Ysize - yr
        # Setting these targets to, e.g., 0.05*xr does not seem to help.
        xm = 0
        ym = 0

        shared_x = self in self._shared_axes["x"]
        shared_y = self in self._shared_axes["y"]

        if shared_x and shared_y:
            raise RuntimeError("set_aspect(..., adjustable='datalim') or "
                               "axis('equal') are not allowed when both axes "
                               "are shared.  Try set_aspect(..., "
                               "adjustable='box').")

        # If y is shared, then we are only allowed to change x, etc.
        if shared_y:
            adjust_y = False
        else:
            if xmarg > xm and ymarg > ym:
                adjy = ((Ymarg > 0 and y_expander < 0) or
                        (Xmarg < 0 and y_expander > 0))
            else:
                adjy = y_expander > 0
            adjust_y = shared_x or adjy  # (Ymarg > xmarg)

        if adjust_y:
            yc = 0.5 * (ymin + ymax)
            y0 = yc - Ysize / 2.0
            y1 = yc + Ysize / 2.0
            if not self.get_autoscaley_on():
                _log.warning("Ignoring fixed y limits to fulfill fixed data aspect "
                             "with adjustable data limits.")
            self.set_ybound(y_trf.inverted().transform([y0, y1]))
        else:
            xc = 0.5 * (xmin + xmax)
            x0 = xc - Xsize / 2.0
            x1 = xc + Xsize / 2.0
            if not self.get_autoscalex_on():
                _log.warning("Ignoring fixed x limits to fulfill fixed data aspect "
                             "with adjustable data limits.")
            self.set_xbound(x_trf.inverted().transform([x0, x1]))
