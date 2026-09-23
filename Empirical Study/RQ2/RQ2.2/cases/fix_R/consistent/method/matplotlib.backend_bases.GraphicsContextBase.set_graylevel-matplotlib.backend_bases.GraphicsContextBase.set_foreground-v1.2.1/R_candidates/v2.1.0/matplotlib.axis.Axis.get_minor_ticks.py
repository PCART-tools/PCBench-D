    def get_minor_ticks(self, numticks=None):
        'get the minor tick instances; grow as necessary'
        if numticks is None:
            numticks = len(self.get_minor_locator()())

        if len(self.minorTicks) < numticks:
            # update the new tick label properties from the old
            for i in range(numticks - len(self.minorTicks)):
                tick = self._get_tick(major=False)
                self.minorTicks.append(tick)

        if self._lastNumMinorTicks < numticks:
            protoTick = self.minorTicks[0]
            for i in range(self._lastNumMinorTicks, len(self.minorTicks)):
                tick = self.minorTicks[i]
                if self._gridOnMinor:
                    tick.gridOn = True
                self._copy_tick_props(protoTick, tick)

        self._lastNumMinorTicks = numticks
        ticks = self.minorTicks[:numticks]

        return ticks
