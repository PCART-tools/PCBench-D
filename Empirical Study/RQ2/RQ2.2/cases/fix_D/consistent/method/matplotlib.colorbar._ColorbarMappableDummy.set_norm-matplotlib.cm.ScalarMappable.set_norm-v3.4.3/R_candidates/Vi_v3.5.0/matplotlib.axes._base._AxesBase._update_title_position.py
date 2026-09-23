    def _update_title_position(self, renderer):
        """
        Update the title position based on the bounding box enclosing
        all the ticklabels and x-axis spine and xlabel...
        """
        if self._autotitlepos is not None and not self._autotitlepos:
            _log.debug('title position was updated manually, not adjusting')
            return

        titles = (self.title, self._left_title, self._right_title)

        for title in titles:
            x, _ = title.get_position()
            # need to start again in case of window resizing
            title.set_position((x, 1.0))
            # need to check all our twins too...
            axs = self._twinned_axes.get_siblings(self)
            # and all the children
            for ax in self.child_axes:
                if ax is not None:
                    locator = ax.get_axes_locator()
                    if locator:
                        pos = locator(self, renderer)
                        ax.apply_aspect(pos)
                    else:
                        ax.apply_aspect()
                    axs = axs + [ax]
            top = -np.Inf
            for ax in axs:
                if (ax.xaxis.get_ticks_position() in ['top', 'unknown']
                        or ax.xaxis.get_label_position() == 'top'):
                    bb = ax.xaxis.get_tightbbox(renderer)
                else:
                    bb = ax.get_window_extent(renderer)
                if bb is not None:
                    top = max(top, bb.ymax)
            if top < 0:
                # the top of Axes is not even on the figure, so don't try and
                # automatically place it.
                _log.debug('top of Axes not in the figure, so title not moved')
                return
            if title.get_window_extent(renderer).ymin < top:
                _, y = self.transAxes.inverted().transform((0, top))
                title.set_position((x, y))
                # empirically, this doesn't always get the min to top,
                # so we need to adjust again.
                if title.get_window_extent(renderer).ymin < top:
                    _, y = self.transAxes.inverted().transform(
                        (0., 2 * top - title.get_window_extent(renderer).ymin))
                    title.set_position((x, y))

        ymax = max(title.get_position()[1] for title in titles)
        for title in titles:
            # now line up all the titles at the highest baseline.
            x, _ = title.get_position()
            title.set_position((x, ymax))
