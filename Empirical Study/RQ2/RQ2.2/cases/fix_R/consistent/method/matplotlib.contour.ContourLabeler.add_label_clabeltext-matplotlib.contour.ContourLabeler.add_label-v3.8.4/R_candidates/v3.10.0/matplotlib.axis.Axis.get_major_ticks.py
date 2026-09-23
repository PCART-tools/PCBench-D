    def get_major_ticks(self, numticks=None):
        r"""
        Return the list of major `.Tick`\s.

        .. warning::

            Ticks are not guaranteed to be persistent. Various operations
            can create, delete and modify the Tick instances. There is an
            imminent risk that changes to individual ticks will not
            survive if you work on the figure further (including also
            panning/zooming on a displayed figure).

            Working on the individual ticks is a method of last resort.
            Use `.set_tick_params` instead if possible.
        """
        if numticks is None:
            numticks = len(self.get_majorticklocs())

        while len(self.majorTicks) < numticks:
            # Update the new tick label properties from the old.
            tick = self._get_tick(major=True)
            self.majorTicks.append(tick)
            self._copy_tick_props(self.majorTicks[0], tick)

        return self.majorTicks[:numticks]
