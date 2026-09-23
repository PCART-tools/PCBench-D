    def get_major_ticks(self, numticks=None):
        'Get the tick instances; grow as necessary.'
        if numticks is None:
            numticks = len(self.get_majorticklocs())

        while len(self.majorTicks) < numticks:
            # Update the new tick label properties from the old.
            tick = self._get_tick(major=True)
            self.majorTicks.append(tick)
            tick.gridline.set_visible(self._gridOnMajor)
            self._copy_tick_props(self.majorTicks[0], tick)

        return self.majorTicks[:numticks]
