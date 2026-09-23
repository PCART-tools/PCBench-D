    def _value_in_bounds(self, val):
        """Makes sure *val* is with given bounds."""
        if self.valstep:
            val = (self.valmin
                   + round((val - self.valmin) / self.valstep) * self.valstep)

        if val <= self.valmin:
            if not self.closedmin:
                return
            val = self.valmin
        elif val >= self.valmax:
            if not self.closedmax:
                return
            val = self.valmax

        if self.slidermin is not None and val <= self.slidermin.val:
            if not self.closedmin:
                return
            val = self.slidermin.val

        if self.slidermax is not None and val >= self.slidermax.val:
            if not self.closedmax:
                return
            val = self.slidermax.val
        return val
