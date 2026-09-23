    def minorticks_off(self):
        """Turn the minor ticks of the colorbar off."""
        ax = self.ax
        long_axis = ax.yaxis if self.orientation == 'vertical' else ax.xaxis
        long_axis.set_minor_locator(ticker.NullLocator())
