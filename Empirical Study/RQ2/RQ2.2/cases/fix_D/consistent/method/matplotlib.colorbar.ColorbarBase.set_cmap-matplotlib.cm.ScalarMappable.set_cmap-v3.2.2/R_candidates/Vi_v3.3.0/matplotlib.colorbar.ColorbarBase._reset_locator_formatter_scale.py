    def _reset_locator_formatter_scale(self):
        """
        Reset the locator et al to defaults.  Any user-hardcoded changes
        need to be re-entered if this gets called (either at init, or when
        the mappable normal gets changed: Colorbar.update_normal)
        """
        self.locator = None
        self.formatter = None
        if isinstance(self.norm, colors.LogNorm):
            # *both* axes are made log so that determining the
            # mid point is easier.
            self.ax.set_xscale('log')
            self.ax.set_yscale('log')
            self.minorticks_on()
            self.__scale = 'log'
        else:
            self.ax.set_xscale('linear')
            self.ax.set_yscale('linear')
            if type(self.norm) is colors.Normalize:
                self.__scale = 'linear'
            else:
                self.__scale = 'manual'
