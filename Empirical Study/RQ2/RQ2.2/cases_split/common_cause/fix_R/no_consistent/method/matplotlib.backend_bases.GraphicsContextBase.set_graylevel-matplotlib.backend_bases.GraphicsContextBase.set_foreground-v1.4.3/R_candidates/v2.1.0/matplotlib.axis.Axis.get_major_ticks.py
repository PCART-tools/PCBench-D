    def get_major_ticks(self, numticks=None):
        'get the tick instances; grow as necessary'
        if numticks is None:
            numticks = len(self.get_major_locator()())
        if len(self.majorTicks) < numticks:
            # update the new tick label properties from the old
            for i in range(numticks - len(self.majorTicks)):
                tick = self._get_tick(major=True)
                self.majorTicks.append(tick)

        if self._lastNumMajorTicks < numticks:
            protoTick = self.majorTicks[0]
            for i in range(self._lastNumMajorTicks, len(self.majorTicks)):
                tick = self.majorTicks[i]
                if self._gridOnMajor:
                    tick.gridOn = True
                self._copy_tick_props(protoTick, tick)

        self._lastNumMajorTicks = numticks
        ticks = self.majorTicks[:numticks]

        return ticks
