    def get_ticks(self, minor=False):
        """Return the x ticks as a list of locations."""
        if self._manual_tick_data_values is None:
            ax = self.ax
            if self.orientation == 'vertical':
                long_axis, short_axis = ax.yaxis, ax.xaxis
            else:
                long_axis, short_axis = ax.xaxis, ax.yaxis
            return long_axis.get_majorticklocs()
        else:
            # We made the axes manually, the old way, and the ylim is 0-1,
            # so the majorticklocs are in those units, not data units.
            return self._manual_tick_data_values
