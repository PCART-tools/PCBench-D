    def get_minor_ticks(self, numticks=None):
        'get the minor tick instances; grow as necessary'
        if numticks is None:
            numticks = len(self.get_minor_locator()())

        while len(self.minorTicks) < numticks:
            # update the new tick label properties from the old
            tick = self._get_tick(major=False)
            self.minorTicks.append(tick)
            if self._gridOnMinor:
                tick.gridOn = True
            self._copy_tick_props(self.minorTicks[0], tick)

        return self.minorTicks[:numticks]
