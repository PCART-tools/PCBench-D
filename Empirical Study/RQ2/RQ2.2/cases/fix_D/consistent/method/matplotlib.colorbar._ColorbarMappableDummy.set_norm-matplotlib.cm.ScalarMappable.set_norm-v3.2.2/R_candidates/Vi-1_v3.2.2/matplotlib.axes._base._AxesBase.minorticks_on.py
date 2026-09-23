    def minorticks_on(self):
        """
        Display minor ticks on the axes.

        Displaying minor ticks may reduce performance; you may turn them off
        using `minorticks_off()` if drawing speed is a problem.
        """
        for ax in (self.xaxis, self.yaxis):
            scale = ax.get_scale()
            if scale == 'log':
                s = ax._scale
                ax.set_minor_locator(mticker.LogLocator(s.base, s.subs))
            elif scale == 'symlog':
                s = ax._scale
                ax.set_minor_locator(
                    mticker.SymmetricalLogLocator(s._transform, s.subs))
            else:
                ax.set_minor_locator(mticker.AutoMinorLocator())
