    def set_units(self, u):
        """
        Set the units for axis.

        Parameters
        ----------
        u : units tag
        """
        if u == self.units:
            return
        self.units = u
        self._update_axisinfo()
        self.callbacks.process('units')
        self.callbacks.process('units finalize')
        self.stale = True
