    def get_minor_ticks(self, numticks=None):
        r"""Return the list of minor `.Tick`\s."""
        if numticks is None:
            numticks = len(self.get_minorticklocs())

        while len(self.minorTicks) < numticks:
            # Update the new tick label properties from the old.
            tick = self._get_tick(major=False)
            self.minorTicks.append(tick)
            tick.gridline.set_visible(self._gridOnMinor)
            self._copy_tick_props(self.minorTicks[0], tick)

        return self.minorTicks[:numticks]
