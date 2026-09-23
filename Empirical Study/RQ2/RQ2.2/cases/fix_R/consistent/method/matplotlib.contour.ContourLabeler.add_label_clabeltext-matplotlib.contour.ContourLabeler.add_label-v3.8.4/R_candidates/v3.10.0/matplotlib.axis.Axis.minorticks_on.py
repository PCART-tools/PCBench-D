    def minorticks_on(self):
        """
        Display default minor ticks on the Axis, depending on the scale
        (`~.axis.Axis.get_scale`).

        Scales use specific minor locators:

        - log: `~.LogLocator`
        - symlog: `~.SymmetricalLogLocator`
        - asinh: `~.AsinhLocator`
        - logit: `~.LogitLocator`
        - default: `~.AutoMinorLocator`

        Displaying minor ticks may reduce performance; you may turn them off
        using `minorticks_off()` if drawing speed is a problem.
        """
        scale = self.get_scale()
        if scale == 'log':
            s = self._scale
            self.set_minor_locator(mticker.LogLocator(s.base, s.subs))
        elif scale == 'symlog':
            s = self._scale
            self.set_minor_locator(
                mticker.SymmetricalLogLocator(s._transform, s.subs))
        elif scale == 'asinh':
            s = self._scale
            self.set_minor_locator(
                    mticker.AsinhLocator(s.linear_width, base=s._base,
                                         subs=s._subs))
        elif scale == 'logit':
            self.set_minor_locator(mticker.LogitLocator(minor=True))
        else:
            self.set_minor_locator(mticker.AutoMinorLocator())
