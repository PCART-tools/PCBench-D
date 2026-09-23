    def minorticks_off(self):
        """
        Turns off the minor ticks on the colorbar.
        """
        ax = self.ax
        long_axis = ax.yaxis if self.orientation == 'vertical' else ax.xaxis

        if long_axis.get_scale() == 'log':
            warnings.warn('minorticks_off() has no effect on a '
                          'logarithmic colorbar axis')
        else:
            long_axis.set_minor_locator(ticker.NullLocator())
