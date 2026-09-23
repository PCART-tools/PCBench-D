    def _remove_axes(self, ax, owners):
        """
        Common helper for removal of standard axes (via delaxes) and of child axes.

        Parameters
        ----------
        ax : `~.AxesBase`
            The Axes to remove.
        owners
            List of objects (list or _AxesStack) "owning" the axes, from which the Axes
            will be remove()d.
        """
        for owner in owners:
            owner.remove(ax)

        self._axobservers.process("_axes_change_event", self)
        self.stale = True
        self.canvas.release_mouse(ax)

        for name in ax._axis_names:  # Break link between any shared axes
            grouper = ax._shared_axes[name]
            siblings = [other for other in grouper.get_siblings(ax) if other is not ax]
            if not siblings:  # Axes was not shared along this axis; we're done.
                continue
            grouper.remove(ax)
            # Formatters and locators may previously have been associated with the now
            # removed axis.  Update them to point to an axis still there (we can pick
            # any of them, and use the first sibling).
            remaining_axis = siblings[0]._axis_map[name]
            remaining_axis.get_major_formatter().set_axis(remaining_axis)
            remaining_axis.get_major_locator().set_axis(remaining_axis)
            remaining_axis.get_minor_formatter().set_axis(remaining_axis)
            remaining_axis.get_minor_locator().set_axis(remaining_axis)

        ax._twinned_axes.remove(ax)  # Break link between any twinned axes.
