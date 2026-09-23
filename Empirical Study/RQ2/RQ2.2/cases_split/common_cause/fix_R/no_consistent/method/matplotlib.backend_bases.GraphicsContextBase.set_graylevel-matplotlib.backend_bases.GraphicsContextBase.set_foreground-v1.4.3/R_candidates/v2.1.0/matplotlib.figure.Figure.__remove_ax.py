    def __remove_ax(self, ax):
        def _reset_loc_form(axis):
            axis.set_major_formatter(axis.get_major_formatter())
            axis.set_major_locator(axis.get_major_locator())
            axis.set_minor_formatter(axis.get_minor_formatter())
            axis.set_minor_locator(axis.get_minor_locator())

        def _break_share_link(ax, grouper):
            siblings = grouper.get_siblings(ax)
            if len(siblings) > 1:
                grouper.remove(ax)
                for last_ax in siblings:
                    if ax is last_ax:
                        continue
                    return last_ax
            return None

        self.delaxes(ax)
        last_ax = _break_share_link(ax, ax._shared_y_axes)
        if last_ax is not None:
            _reset_loc_form(last_ax.yaxis)

        last_ax = _break_share_link(ax, ax._shared_x_axes)
        if last_ax is not None:
            _reset_loc_form(last_ax.xaxis)
