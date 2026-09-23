    def config_axis(self):
        ax = self.ax
        if (isinstance(self.norm, colors.LogNorm)
                and self._use_auto_colorbar_locator()):
            # *both* axes are made log so that determining the
            # mid point is easier.
            ax.set_xscale('log')
            ax.set_yscale('log')

        if self.orientation == 'vertical':
            long_axis, short_axis = ax.yaxis, ax.xaxis
        else:
            long_axis, short_axis = ax.xaxis, ax.yaxis

        long_axis.set_label_position(self.ticklocation)
        long_axis.set_ticks_position(self.ticklocation)
        short_axis.set_ticks([])
        short_axis.set_ticks([], minor=True)

        self._set_label()
