    def _set_order_of_magnitude(self):
        # if scientific notation is to be used, find the appropriate exponent
        # if using a numerical offset, find the exponent after applying the
        # offset. When lower power limit = upper <> 0, use provided exponent.
        if not self._scientific:
            self.orderOfMagnitude = 0
            return
        if self._powerlimits[0] == self._powerlimits[1] != 0:
            # fixed scaling when lower power limit = upper <> 0.
            self.orderOfMagnitude = self._powerlimits[0]
            return
        # restrict to visible ticks
        vmin, vmax = sorted(self.axis.get_view_interval())
        locs = np.asarray(self.locs)
        locs = locs[(vmin <= locs) & (locs <= vmax)]
        locs = np.abs(locs)
        if not len(locs):
            self.orderOfMagnitude = 0
            return
        if self.offset:
            oom = math.floor(math.log10(vmax - vmin))
        else:
            val = locs.max()
            if val == 0:
                oom = 0
            else:
                oom = math.floor(math.log10(val))
        if oom <= self._powerlimits[0]:
            self.orderOfMagnitude = oom
        elif oom >= self._powerlimits[1]:
            self.orderOfMagnitude = oom
        else:
            self.orderOfMagnitude = 0
