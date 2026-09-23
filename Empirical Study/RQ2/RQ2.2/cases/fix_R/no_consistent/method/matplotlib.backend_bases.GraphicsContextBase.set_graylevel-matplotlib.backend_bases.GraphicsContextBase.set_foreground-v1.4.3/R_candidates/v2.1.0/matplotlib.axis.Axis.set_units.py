    def set_units(self, u):
        """
        set the units for axis

        ACCEPTS: a units tag
        """
        pchanged = False
        if u is None:
            self.units = None
            pchanged = True
        else:
            if u != self.units:
                self.units = u
                pchanged = True
        if pchanged:
            self._update_axisinfo()
            self.callbacks.process('units')
            self.callbacks.process('units finalize')
        self.stale = True
