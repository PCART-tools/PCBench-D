    def set_ylim(self, bottom=None, top=None, emit=True, auto=False,
                 *, ymin=None, ymax=None):
        """
        Set the data limits for the y-axis

        .. ACCEPTS: (bottom: float, top: float)

        Parameters
        ----------
        bottom : scalar, optional
            The bottom ylim (default: None, which leaves the bottom
            limit unchanged).
            The bottom and top ylims may be passed as the tuple
            (`bottom`, `top`) as the first positional argument (or as
            the `bottom` keyword argument).

        top : scalar, optional
            The top ylim (default: None, which leaves the top limit
            unchanged).

        emit : bool, optional
            Whether to notify observers of limit change (default: True).

        auto : bool or None, optional
            Whether to turn on autoscaling of the y-axis. True turns on,
            False turns off (default action), None leaves unchanged.

        ymin, ymax : scalar, optional
            These arguments are deprecated and will be removed in a future
            version.  They are equivalent to bottom and top respectively,
            and it is an error to pass both `xmin` and `bottom` or
            `xmax` and `top`.

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
        if top is None and iterable(bottom):
            bottom, top = bottom
        if ymin is not None:
            cbook.warn_deprecated('3.0', name='`ymin`',
                                  alternative='`bottom`', obj_type='argument')
            if bottom is not None:
                raise TypeError('Cannot pass both `ymin` and `bottom`')
            bottom = ymin
        if ymax is not None:
            cbook.warn_deprecated('3.0', name='`ymax`',
                                  alternative='`top`', obj_type='argument')
            if top is not None:
                raise TypeError('Cannot pass both `ymax` and `top`')
            top = ymax

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
                 'bottom=%s, top=%s') % (bottom, top), stacklevel=2)

        bottom, top = mtransforms.nonsingular(bottom, top, increasing=False)

        if self.get_yscale() == 'log':
            if bottom <= 0:
                warnings.warn(
                    'Attempted to set non-positive bottom ylim on a '
                    'log-scaled axis.\n'
                    'Invalid limit will be ignored.', stacklevel=2)
                bottom = old_bottom
            if top <= 0:
                warnings.warn(
                    'Attempted to set non-positive top ylim on a '
                    'log-scaled axis.\n'
                    'Invalid limit will be ignored.', stacklevel=2)
                top = old_top
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
