    def _set_scale(self):
        """
        Check if parent has set its scale
        """

        if self._orientation == 'x':
            pscale = self._parent.xaxis.get_scale()
            set_scale = self.set_xscale
        else:  # 'y'
            pscale = self._parent.yaxis.get_scale()
            set_scale = self.set_yscale
        if pscale == self._parentscale:
            return

        if self._ticks_set:
            ticks = self._axis.get_ticklocs()

        # need to invert the roles here for the ticks to line up.
        set_scale('functionlog' if pscale == 'log' else 'function',
                  functions=self._functions[::-1])

        # OK, set_scale sets the locators, but if we've called
        # axsecond.set_ticks, we want to keep those.
        if self._ticks_set:
            self._axis.set_major_locator(mticker.FixedLocator(ticks))

        # If the parent scale doesn't change, we can skip this next time.
        self._parentscale = pscale
