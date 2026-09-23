    def minorticks_off(self):
        """
        Turns off the minor ticks on the colorbar.
        """
        ax = self.ax
        long_axis = ax.yaxis if self.orientation == 'vertical' else ax.xaxis

        long_axis.set_minor_locator(ticker.NullLocator())
