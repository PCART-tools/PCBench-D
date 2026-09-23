    def delaxes(self, ax):
        """
        Remove the `~.axes.Axes` *ax* from the figure; update the current Axes.
        """

        def _reset_locators_and_formatters(axis):
            # Set the formatters and locators to be associated with axis
            # (where previously they may have been associated with another
            # Axis instance)
            axis.get_major_formatter().set_axis(axis)
            axis.get_major_locator().set_axis(axis)
            axis.get_minor_formatter().set_axis(axis)
            axis.get_minor_locator().set_axis(axis)

        def _break_share_link(ax, grouper):
            siblings = grouper.get_siblings(ax)
            if len(siblings) > 1:
                grouper.remove(ax)
                for last_ax in siblings:
                    if ax is not last_ax:
                        return last_ax
            return None

        self._axstack.remove(ax)
        self._axobservers.process("_axes_change_event", self)
        self.stale = True
        self._localaxes.remove(ax)

        # Break link between any shared axes
        for name in ax._axis_names:
            last_ax = _break_share_link(ax, ax._shared_axes[name])
            if last_ax is not None:
                _reset_locators_and_formatters(getattr(last_ax, f"{name}axis"))

        # Break link between any twinned axes
        _break_share_link(ax, ax._twinned_axes)
