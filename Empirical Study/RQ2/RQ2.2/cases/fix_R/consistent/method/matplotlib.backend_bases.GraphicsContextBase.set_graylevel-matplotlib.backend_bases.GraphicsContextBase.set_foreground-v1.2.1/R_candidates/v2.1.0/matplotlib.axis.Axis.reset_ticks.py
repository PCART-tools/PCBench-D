    def reset_ticks(self):
        # build a few default ticks; grow as necessary later; only
        # define 1 so properties set on ticks will be copied as they
        # grow
        del self.majorTicks[:]
        del self.minorTicks[:]

        self.majorTicks.extend([self._get_tick(major=True)])
        self.minorTicks.extend([self._get_tick(major=False)])
        self._lastNumMajorTicks = 1
        self._lastNumMinorTicks = 1
