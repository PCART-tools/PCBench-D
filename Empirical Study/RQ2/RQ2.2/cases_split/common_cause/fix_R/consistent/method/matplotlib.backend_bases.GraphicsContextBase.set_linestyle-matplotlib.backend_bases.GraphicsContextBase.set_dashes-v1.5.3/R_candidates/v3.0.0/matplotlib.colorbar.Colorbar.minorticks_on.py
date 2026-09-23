    def minorticks_on(self):
        """
        Turns on the minor ticks on the colorbar without extruding
        into the "extend regions".
        """
        ax = self.ax
        long_axis = ax.yaxis if self.orientation == 'vertical' else ax.xaxis

        if long_axis.get_scale() == 'log':
            warnings.warn('minorticks_on() has no effect on a '
                          'logarithmic colorbar axis')
        else:
            long_axis.set_minor_locator(_ColorbarAutoMinorLocator(self))
