    def autoscale_view(self, tight=None, scalex=True, scaley=True):
        """
        Autoscale the view limits using the data limits.

        Parameters
        ----------
        tight : bool or None
            If *True*, only expand the axis limits using the margins.  Note
            that unlike for `autoscale`, ``tight=True`` does *not* set the
            margins to zero.

            If *False* and :rc:`axes.autolimit_mode` is 'round_numbers', then
            after expansion by the margins, further expand the axis limits
            using the axis major locator.

            If None (the default), reuse the value set in the previous call to
            `autoscale_view` (the initial value is False, but the default style
            sets :rc:`axes.autolimit_mode` to 'data', in which case this
            behaves like True).

        scalex : bool, default: True
            Whether to autoscale the x axis.

        scaley : bool, default: True
            Whether to autoscale the y axis.

        Notes
        -----
        The autoscaling preserves any preexisting axis direction reversal.

        The data limits are not updated automatically when artist data are
        changed after the artist has been added to an Axes instance.  In that
        case, use :meth:`matplotlib.axes.Axes.relim` prior to calling
        autoscale_view.

        If the views of the axes are fixed, e.g. via `set_xlim`, they will
        not be changed by autoscale_view().
        See :meth:`matplotlib.axes.Axes.autoscale` for an alternative.
        """
        if tight is not None:
            self._tight = bool(tight)

        x_stickies = y_stickies = np.array([])
        if self.use_sticky_edges:
            # Only iterate over axes and artists if needed.  The check for
            # ``hasattr(ax, "lines")`` is necessary because this can be called
            # very early in the axes init process (e.g., for twin axes) when
            # these attributes don't even exist yet, in which case
            # `get_children` would raise an AttributeError.
            if self._xmargin and scalex and self._autoscaleXon:
                x_stickies = np.sort(np.concatenate([
                    artist.sticky_edges.x
                    for ax in self._shared_x_axes.get_siblings(self)
                    if hasattr(ax, "lines")
                    for artist in ax.get_children()]))
            if self._ymargin and scaley and self._autoscaleYon:
                y_stickies = np.sort(np.concatenate([
                    artist.sticky_edges.y
                    for ax in self._shared_y_axes.get_siblings(self)
                    if hasattr(ax, "lines")
                    for artist in ax.get_children()]))
        if self.get_xscale() == 'log':
            x_stickies = x_stickies[x_stickies > 0]
        if self.get_yscale() == 'log':
            y_stickies = y_stickies[y_stickies > 0]

        def handle_single_axis(scale, autoscaleon, shared_axes, interval,
                               minpos, axis, margin, stickies, set_bound):

            if not (scale and autoscaleon):
                return  # nothing to do...

            shared = shared_axes.get_siblings(self)
            # Base autoscaling on finite data limits when there is at least one
            # finite data limit among all the shared_axes and intervals.
            # Also, find the minimum minpos for use in the margin calculation.
            x_values = []
            minimum_minpos = np.inf
            for ax in shared:
                x_values.extend(getattr(ax.dataLim, interval))
                minimum_minpos = min(minimum_minpos,
                                     getattr(ax.dataLim, minpos))
            x_values = np.extract(np.isfinite(x_values), x_values)
            if x_values.size >= 1:
                x0, x1 = (x_values.min(), x_values.max())
            else:
                x0, x1 = (-np.inf, np.inf)
            # If x0 and x1 are non finite, use the locator to figure out
            # default limits.
            locator = axis.get_major_locator()
            x0, x1 = locator.nonsingular(x0, x1)

            # Prevent margin addition from crossing a sticky value.  A small
            # tolerance must be added due to floating point issues with
            # streamplot; it is defined relative to x0, x1, x1-x0 but has
            # no absolute term (e.g. "+1e-8") to avoid issues when working with
            # datasets where all values are tiny (less than 1e-8).
            tol = 1e-5 * max(abs(x0), abs(x1), abs(x1 - x0))
            # Index of largest element < x0 + tol, if any.
            i0 = stickies.searchsorted(x0 + tol) - 1
            x0bound = stickies[i0] if i0 != -1 else None
            # Index of smallest element > x1 - tol, if any.
            i1 = stickies.searchsorted(x1 - tol)
            x1bound = stickies[i1] if i1 != len(stickies) else None

            # Add the margin in figure space and then transform back, to handle
            # non-linear scales.
            transform = axis.get_transform()
            inverse_trans = transform.inverted()
            x0, x1 = axis._scale.limit_range_for_scale(x0, x1, minimum_minpos)
            x0t, x1t = transform.transform([x0, x1])
            delta = (x1t - x0t) * margin
            if not np.isfinite(delta):
                delta = 0  # If a bound isn't finite, set margin to zero.
            x0, x1 = inverse_trans.transform([x0t - delta, x1t + delta])

            # Apply sticky bounds.
            if x0bound is not None:
                x0 = max(x0, x0bound)
            if x1bound is not None:
                x1 = min(x1, x1bound)

            if not self._tight:
                x0, x1 = locator.view_limits(x0, x1)
            set_bound(x0, x1)
            # End of definition of internal function 'handle_single_axis'.

        handle_single_axis(
            scalex, self._autoscaleXon, self._shared_x_axes, 'intervalx',
            'minposx', self.xaxis, self._xmargin, x_stickies, self.set_xbound)
        handle_single_axis(
            scaley, self._autoscaleYon, self._shared_y_axes, 'intervaly',
            'minposy', self.yaxis, self._ymargin, y_stickies, self.set_ybound)
