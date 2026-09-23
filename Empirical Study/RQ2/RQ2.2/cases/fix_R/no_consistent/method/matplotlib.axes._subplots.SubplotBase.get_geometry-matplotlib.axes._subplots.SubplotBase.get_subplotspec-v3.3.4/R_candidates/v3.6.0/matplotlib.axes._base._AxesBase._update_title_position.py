    def _update_title_position(self, renderer):
        """
        Update the title position based on the bounding box enclosing
        all the ticklabels and x-axis spine and xlabel...
        """
        if self._autotitlepos is not None and not self._autotitlepos:
            _log.debug('title position was updated manually, not adjusting')
            return

        titles = (self.title, self._left_title, self._right_title)

        # Need to check all our twins too, and all the children as well.
        axs = self._twinned_axes.get_siblings(self) + self.child_axes
        for ax in self.child_axes:  # Child positions must be updated first.
            locator = ax.get_axes_locator()
            ax.apply_aspect(locator(self, renderer) if locator else None)

        for title in titles:
            x, _ = title.get_position()
            # need to start again in case of window resizing
            title.set_position((x, 1.0))
            top = -np.inf
            for ax in axs:
                bb = None
                if (ax.xaxis.get_ticks_position() in ['top', 'unknown']
                        or ax.xaxis.get_label_position() == 'top'):
                    bb = ax.xaxis.get_tightbbox(renderer)
                if bb is None:
                    if 'outline' in ax.spines:
                        # Special case for colorbars:
                        bb = ax.spines['outline'].get_window_extent()
                    else:
                        bb = ax.get_window_extent(renderer)
                top = max(top, bb.ymax)
                if title.get_text():
                    ax.yaxis.get_tightbbox(renderer)  # update offsetText
                    if ax.yaxis.offsetText.get_text():
                        bb = ax.yaxis.offsetText.get_tightbbox(renderer)
                        if bb.intersection(title.get_tightbbox(renderer), bb):
                            top = bb.ymax
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
