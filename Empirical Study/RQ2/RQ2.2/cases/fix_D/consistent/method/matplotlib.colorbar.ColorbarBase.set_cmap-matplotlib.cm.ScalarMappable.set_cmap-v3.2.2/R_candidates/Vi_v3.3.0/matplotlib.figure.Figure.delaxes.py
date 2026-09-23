    def delaxes(self, ax):
        """
        Remove the `~.axes.Axes` *ax* from the figure; update the current axes.
        """

        def _reset_locators_and_formatters(axis):
            # Set the formatters and locators to be associated with axis
            # (where previously they may have been associated with another
            # Axis instance)
            #
            # Because set_major_formatter() etc. force isDefault_* to be False,
            # we have to manually check if the original formatter was a
            # default and manually set isDefault_* if that was the case.
            majfmt = axis.get_major_formatter()
            isDefault = majfmt.axis.isDefault_majfmt
            axis.set_major_formatter(majfmt)
            if isDefault:
                majfmt.axis.isDefault_majfmt = True

            majloc = axis.get_major_locator()
            isDefault = majloc.axis.isDefault_majloc
            axis.set_major_locator(majloc)
            if isDefault:
                majloc.axis.isDefault_majloc = True

            minfmt = axis.get_minor_formatter()
            isDefault = majloc.axis.isDefault_minfmt
            axis.set_minor_formatter(minfmt)
            if isDefault:
                minfmt.axis.isDefault_minfmt = True

            minloc = axis.get_minor_locator()
            isDefault = majloc.axis.isDefault_minloc
            axis.set_minor_locator(minloc)
            if isDefault:
                minloc.axis.isDefault_minloc = True

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

        last_ax = _break_share_link(ax, ax._shared_y_axes)
        if last_ax is not None:
            _reset_locators_and_formatters(last_ax.yaxis)

        last_ax = _break_share_link(ax, ax._shared_x_axes)
        if last_ax is not None:
            _reset_locators_and_formatters(last_ax.xaxis)
