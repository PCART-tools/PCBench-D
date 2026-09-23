    def _config_axis(self):
        """Set up long and short axis."""
        ax = self.ax
        if self.orientation == 'vertical':
            long_axis, short_axis = ax.yaxis, ax.xaxis
            if mpl.rcParams['ytick.minor.visible']:
                self.minorticks_on()
        else:
            long_axis, short_axis = ax.xaxis, ax.yaxis
            if mpl.rcParams['xtick.minor.visible']:
                self.minorticks_on()
        long_axis.set(label_position=self.ticklocation,
                      ticks_position=self.ticklocation)
        short_axis.set_ticks([])
        short_axis.set_ticks([], minor=True)
        self._set_label()
