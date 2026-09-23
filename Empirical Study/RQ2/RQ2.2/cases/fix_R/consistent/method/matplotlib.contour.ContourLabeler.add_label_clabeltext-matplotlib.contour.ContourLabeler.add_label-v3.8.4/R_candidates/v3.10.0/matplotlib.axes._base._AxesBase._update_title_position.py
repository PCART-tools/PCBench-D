    def _update_title_position(self, renderer):
        """
        Update the title position based on the bounding box enclosing
        all the ticklabels and x-axis spine and xlabel...
        """
        if self._autotitlepos is not None and not self._autotitlepos:
            _log.debug('title position was updated manually, not adjusting')
            return

        titles = (self.title, self._left_title, self._right_title)

        if not any(title.get_text() for title in titles):
            # If the titles are all empty, there is no need to update their positions.
            return

        # Need to check all our twins too, aligned axes, and all the children
        # as well.
        axs = set()
        axs.update(self.child_axes)
        axs.update(self._twinned_axes.get_siblings(self))
        axs.update(
            self.get_figure(root=False)._align_label_groups['title'].get_siblings(self))

        for ax in self.child_axes:  # Child positions must be updated first.
            locator = ax.get_axes_locator()
            ax.apply_aspect(locator(self, renderer) if locator else None)

        top = -np.inf
        for ax in axs:
            bb = None
            xticklabel_top = any(tick.label2.get_visible() for tick in
                                 [ax.xaxis.majorTicks[0], ax.xaxis.minorTicks[0]])
            if (xticklabel_top or ax.xaxis.get_label_position() == 'top'):
                bb = ax.xaxis.get_tightbbox(renderer)
            if bb is None:
                # Extent of the outline for colorbars, of the axes otherwise.
                bb = ax.spines.get("outline", ax).get_window_extent()
            top = max(top, bb.ymax)

        for title in titles:
            x, _ = title.get_position()
            # need to start again in case of window resizing
            title.set_position((x, 1.0))
            if title.get_text():
                for ax in axs:
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
