    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        return RadialTick(self.axes, 0, major=major, **tick_kw)
