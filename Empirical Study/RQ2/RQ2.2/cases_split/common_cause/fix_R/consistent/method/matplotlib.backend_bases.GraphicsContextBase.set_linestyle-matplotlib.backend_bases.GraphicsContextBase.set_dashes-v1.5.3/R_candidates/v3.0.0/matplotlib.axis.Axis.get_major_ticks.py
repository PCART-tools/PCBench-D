    def get_major_ticks(self, numticks=None):
        'get the tick instances; grow as necessary'
        if numticks is None:
            numticks = len(self.get_major_locator()())

        while len(self.majorTicks) < numticks:
            # update the new tick label properties from the old
            tick = self._get_tick(major=True)
            self.majorTicks.append(tick)
            if self._gridOnMajor:
                tick.gridOn = True
            self._copy_tick_props(self.majorTicks[0], tick)

        return self.majorTicks[:numticks]
