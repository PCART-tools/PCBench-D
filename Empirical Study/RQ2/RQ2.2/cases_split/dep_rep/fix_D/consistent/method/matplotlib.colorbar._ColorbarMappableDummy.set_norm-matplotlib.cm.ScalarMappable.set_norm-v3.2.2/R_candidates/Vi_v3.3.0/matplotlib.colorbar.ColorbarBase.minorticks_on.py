    def minorticks_on(self):
        """
        Turn the minor ticks of the colorbar on without extruding
        into the "extend regions".
        """
        ax = self.ax
        long_axis = ax.yaxis if self.orientation == 'vertical' else ax.xaxis

        if long_axis.get_scale() == 'log':
            long_axis.set_minor_locator(_ColorbarLogLocator(self, base=10.,
                                                            subs='auto'))
            long_axis.set_minor_formatter(ticker.LogFormatterSciNotation())
        else:
            long_axis.set_minor_locator(_ColorbarAutoMinorLocator(self))
