    def autoscale_view(self, tight=None, scalex=True, scaley=True):
        """
        Autoscale the view limits using the data limits. You can
        selectively autoscale only a single axis, e.g., the xaxis by
        setting *scaley* to *False*.  The autoscaling preserves any
        axis direction reversal that has already been done.

        If *tight* is *False*, the axis major locator will be used
        to expand the view limits if rcParams['axes.autolimit_mode']
        is 'round_numbers'.  Note that any margins that are in effect
        will be applied first, regardless of whether *tight* is
        *True* or *False*.  Specifying *tight* as *True* or *False*
        saves the setting as a private attribute of the Axes; specifying
        it as *None* (the default) applies the previously saved value.

        The data limits are not updated automatically when artist data are
        changed after the artist has been added to an Axes instance.  In that
        case, use :meth:`matplotlib.axes.Axes.relim` prior to calling
        autoscale_view.
        """
        if tight is not None:
            self._tight = bool(tight)

        if self.use_sticky_edges and (self._xmargin or self._ymargin):
            stickies = [artist.sticky_edges for artist in self.get_children()]
            x_stickies = sum([sticky.x for sticky in stickies], [])
            y_stickies = sum([sticky.y for sticky in stickies], [])
            if self.get_xscale().lower() == 'log':
                x_stickies = [xs for xs in x_stickies if xs > 0]
            if self.get_yscale().lower() == 'log':
                y_stickies = [ys for ys in y_stickies if ys > 0]
        else:  # Small optimization.
            x_stickies, y_stickies = [], []

        def handle_single_axis(scale, autoscaleon, shared_axes, interval,
                               minpos, axis, margin, stickies, set_bound):

            if not (scale and autoscaleon):
                return  # nothing to do...

            shared = shared_axes.get_siblings(self)
            dl = [ax.dataLim for ax in shared]
            # ignore non-finite data limits if good limits exist
            finite_dl = [d for d in dl if np.isfinite(d).all()]
            if len(finite_dl):
                # if finite limits exist for atleast one axis (and the
                # other is infinite), restore the finite limits
                x_finite = [d for d in dl
                            if (np.isfinite(d.intervalx).all() and
                                (d not in finite_dl))]
                y_finite = [d for d in dl
                            if (np.isfinite(d.intervaly).all() and
                                (d not in finite_dl))]

                dl = finite_dl
                dl.extend(x_finite)
                dl.extend(y_finite)

            bb = mtransforms.BboxBase.union(dl)
            x0, x1 = getattr(bb, interval)
            locator = axis.get_major_locator()
            try:
                # e.g., DateLocator has its own nonsingular()
                x0, x1 = locator.nonsingular(x0, x1)
            except AttributeError:
                # Default nonsingular for, e.g., MaxNLocator
                x0, x1 = mtransforms.nonsingular(
                    x0, x1, increasing=False, expander=0.05)

            # Add the margin in figure space and then transform back, to handle
            # non-linear scales.
            minpos = getattr(bb, minpos)
            transform = axis.get_transform()
            inverse_trans = transform.inverted()
            # We cannot use exact equality due to floating point issues e.g.
            # with streamplot.
            do_lower_margin = not np.any(np.isclose(x0, stickies))
            do_upper_margin = not np.any(np.isclose(x1, stickies))
            x0, x1 = axis._scale.limit_range_for_scale(x0, x1, minpos)
            x0t, x1t = transform.transform([x0, x1])
            delta = (x1t - x0t) * margin
            if do_lower_margin:
                x0t -= delta
            if do_upper_margin:
                x1t += delta
            x0, x1 = inverse_trans.transform([x0t, x1t])

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
