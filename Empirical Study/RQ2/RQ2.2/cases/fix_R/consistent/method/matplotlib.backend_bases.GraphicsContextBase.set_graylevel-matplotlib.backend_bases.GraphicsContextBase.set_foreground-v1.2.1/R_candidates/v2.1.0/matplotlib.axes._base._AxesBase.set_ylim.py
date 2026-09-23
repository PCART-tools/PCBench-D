    def set_ylim(self, bottom=None, top=None, emit=True, auto=False, **kw):
        """
        Set the data limits for the y-axis

        Parameters
        ----------
        bottom : scalar, optional
            The bottom ylim (default: None, which leaves the bottom
            limit unchanged).

        top : scalar, optional
            The top ylim (default: None, which leaves the top limit
            unchanged).

        emit : bool, optional
            Whether to notify observers of limit change (default: True).

        auto : bool or None, optional
            Whether to turn on autoscaling of the y-axis. True turns on,
            False turns off (default action), None leaves unchanged.

        ylimits : tuple, optional
            The bottom and top yxlims may be passed as the tuple
            (`bottom`, `top`) as the first positional argument (or as
            the `bottom` keyword argument).

        Returns
        -------
        ylimits : tuple
            Returns the new y-axis limits as (`bottom`, `top`).

        Notes
        -----
        The `bottom` value may be greater than the `top` value, in which
        case the y-axis values will decrease from bottom to top.

        Examples
        --------
        >>> set_ylim(bottom, top)
        >>> set_ylim((bottom, top))
        >>> bottom, top = set_ylim(bottom, top)

        One limit may be left unchanged.

        >>> set_ylim(top=top_lim)

        Limits may be passed in reverse order to flip the direction of
        the y-axis. For example, suppose `y` represents depth of the
        ocean in m. The y-axis limits might be set like the following
        so 5000 m depth is at the bottom of the plot and the surface,
        0 m, is at the top.

        >>> set_ylim(5000, 0)
        """
        if 'ymin' in kw:
            bottom = kw.pop('ymin')
        if 'ymax' in kw:
            top = kw.pop('ymax')
        if kw:
            raise ValueError("unrecognized kwargs: %s" % list(kw))

        if top is None and iterable(bottom):
            bottom, top = bottom

        bottom = self._validate_converted_limits(bottom, self.convert_yunits)
        top = self._validate_converted_limits(top, self.convert_yunits)

        old_bottom, old_top = self.get_ylim()

        if bottom is None:
            bottom = old_bottom
        if top is None:
            top = old_top

        if bottom == top:
            warnings.warn(
                ('Attempting to set identical bottom==top results\n'
                 'in singular transformations; automatically expanding.\n'
                 'bottom=%s, top=%s') % (bottom, top))

        bottom, top = mtransforms.nonsingular(bottom, top, increasing=False)

        if self.get_yscale() == 'log' and (bottom <= 0.0 or top <= 0.0):
            warnings.warn(
                'Attempted to set non-positive ylimits for log-scale axis; '
                'invalid limits will be ignored.')
        bottom, top = self.yaxis.limit_range_for_scale(bottom, top)

        self.viewLim.intervaly = (bottom, top)
        if auto is not None:
            self._autoscaleYon = bool(auto)

        if emit:
            self.callbacks.process('ylim_changed', self)
            # Call all of the other y-axes that are shared with this one
            for other in self._shared_y_axes.get_siblings(self):
                if other is not self:
                    other.set_ylim(self.viewLim.intervaly,
                                   emit=False, auto=auto)
                    if (other.figure != self.figure and
                            other.figure.canvas is not None):
                        other.figure.canvas.draw_idle()
        self.stale = True
        return bottom, top
