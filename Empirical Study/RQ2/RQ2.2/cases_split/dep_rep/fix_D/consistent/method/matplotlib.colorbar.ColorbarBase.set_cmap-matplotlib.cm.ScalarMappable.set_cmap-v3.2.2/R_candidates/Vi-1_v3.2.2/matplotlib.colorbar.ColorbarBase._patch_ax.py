    def _patch_ax(self):
        # bind some methods to the axes to warn users
        # against using those methods.
        self.ax.set_xticks = _set_ticks_on_axis_warn
        self.ax.set_yticks = _set_ticks_on_axis_warn
