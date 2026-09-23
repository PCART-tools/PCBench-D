    @docstring.copy(Axis.set_ticks)
    def set_ticks(self, ticks, labels=None, *, minor=False, **kwargs):
        ret = self._axis.set_ticks(ticks, labels, minor=minor, **kwargs)
        self.stale = True
        self._ticks_set = True
        return ret
