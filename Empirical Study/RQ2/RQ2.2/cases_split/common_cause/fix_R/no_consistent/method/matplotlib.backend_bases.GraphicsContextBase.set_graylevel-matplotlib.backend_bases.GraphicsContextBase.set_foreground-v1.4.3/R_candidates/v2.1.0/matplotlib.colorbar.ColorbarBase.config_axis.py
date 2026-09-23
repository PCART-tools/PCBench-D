    def config_axis(self):
        ax = self.ax
        if self.orientation == 'vertical':
            ax.xaxis.set_ticks([])
            # location is either one of 'bottom' or 'top'
            ax.yaxis.set_label_position(self.ticklocation)
            ax.yaxis.set_ticks_position(self.ticklocation)
        else:
            ax.yaxis.set_ticks([])
            # location is either one of 'left' or 'right'
            ax.xaxis.set_label_position(self.ticklocation)
            ax.xaxis.set_ticks_position(self.ticklocation)

        self._set_label()
