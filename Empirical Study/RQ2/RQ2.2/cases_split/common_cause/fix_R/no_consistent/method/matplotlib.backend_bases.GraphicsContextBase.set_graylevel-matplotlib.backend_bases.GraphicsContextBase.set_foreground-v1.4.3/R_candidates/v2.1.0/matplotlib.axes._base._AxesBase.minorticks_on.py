    def minorticks_on(self):
        'Add autoscaling minor ticks to the axes.'
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
