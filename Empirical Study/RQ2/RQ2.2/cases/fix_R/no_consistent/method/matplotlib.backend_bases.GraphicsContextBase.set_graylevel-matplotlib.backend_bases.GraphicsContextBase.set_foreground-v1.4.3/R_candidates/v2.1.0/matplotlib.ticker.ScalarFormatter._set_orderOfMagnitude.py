    def _set_orderOfMagnitude(self, range):
        # if scientific notation is to be used, find the appropriate exponent
        # if using an numerical offset, find the exponent after applying the
        # offset
        if not self._scientific:
            self.orderOfMagnitude = 0
            return
        locs = np.abs(self.locs)
        if self.offset:
            oom = math.floor(math.log10(range))
        else:
            if locs[0] > locs[-1]:
                val = locs[0]
            else:
                val = locs[-1]
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
