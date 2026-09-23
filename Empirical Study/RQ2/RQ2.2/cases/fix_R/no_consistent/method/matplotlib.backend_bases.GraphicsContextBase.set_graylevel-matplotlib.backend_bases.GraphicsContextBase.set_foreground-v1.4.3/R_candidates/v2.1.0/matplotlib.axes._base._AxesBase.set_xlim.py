    def set_xlim(self, left=None, right=None, emit=True, auto=False, **kw):
        """
        Set the data limits for the x-axis

        Parameters
        ----------
        left : scalar, optional
            The left xlim (default: None, which leaves the left limit
            unchanged).

        right : scalar, optional
            The right xlim (default: None, which leaves the right limit
            unchanged).

        emit : bool, optional
            Whether to notify observers of limit change (default: True).

        auto : bool or None, optional
            Whether to turn on autoscaling of the x-axis. True turns on,
            False turns off (default action), None leaves unchanged.

        xlimits : tuple, optional
            The left and right xlims may be passed as the tuple
            (`left`, `right`) as the first positional argument (or as
            the `left` keyword argument).

        Returns
        -------
        xlimits : tuple
            Returns the new x-axis limits as (`left`, `right`).

        Notes
        -----
        The `left` value may be greater than the `right` value, in which
        case the x-axis values will decrease from left to right.

        Examples
        --------
        >>> set_xlim(left, right)
        >>> set_xlim((left, right))
        >>> left, right = set_xlim(left, right)

        One limit may be left unchanged.

        >>> set_xlim(right=right_lim)

        Limits may be passed in reverse order to flip the direction of
        the x-axis. For example, suppose `x` represents the number of
        years before present. The x-axis limits might be set like the
        following so 5000 years ago is on the left of the plot and the
        present is on the right.

        >>> set_xlim(5000, 0)

        """
        if 'xmin' in kw:
            left = kw.pop('xmin')
        if 'xmax' in kw:
            right = kw.pop('xmax')
        if kw:
            raise ValueError("unrecognized kwargs: %s" % list(kw))

        if right is None and iterable(left):
            left, right = left

        self._process_unit_info(xdata=(left, right))
        left = self._validate_converted_limits(left, self.convert_xunits)
        right = self._validate_converted_limits(right, self.convert_xunits)

        old_left, old_right = self.get_xlim()
        if left is None:
            left = old_left
        if right is None:
            right = old_right

        if left == right:
            warnings.warn(
                ('Attempting to set identical left==right results\n'
                 'in singular transformations; automatically expanding.\n'
                 'left=%s, right=%s') % (left, right))
        left, right = mtransforms.nonsingular(left, right, increasing=False)

        if self.get_xscale() == 'log' and (left <= 0.0 or right <= 0.0):
            warnings.warn(
                'Attempted to set non-positive xlimits for log-scale axis; '
                'invalid limits will be ignored.')
        left, right = self.xaxis.limit_range_for_scale(left, right)

        self.viewLim.intervalx = (left, right)
        if auto is not None:
            self._autoscaleXon = bool(auto)

        if emit:
            self.callbacks.process('xlim_changed', self)
            # Call all of the other x-axes that are shared with this one
            for other in self._shared_x_axes.get_siblings(self):
                if other is not self:
                    other.set_xlim(self.viewLim.intervalx,
                                   emit=False, auto=auto)
                    if (other.figure != self.figure and
                            other.figure.canvas is not None):
                        other.figure.canvas.draw_idle()
        self.stale = True
        return left, right
