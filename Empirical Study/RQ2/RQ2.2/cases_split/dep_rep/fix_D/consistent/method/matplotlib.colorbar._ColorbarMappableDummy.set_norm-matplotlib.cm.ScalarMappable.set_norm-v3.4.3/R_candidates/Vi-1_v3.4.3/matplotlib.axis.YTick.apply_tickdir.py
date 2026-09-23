    def apply_tickdir(self, tickdir):
        # docstring inherited
        super().apply_tickdir(tickdir)
        self._tickmarkers = {
            'out': (mlines.TICKLEFT, mlines.TICKRIGHT),
            'in': (mlines.TICKRIGHT, mlines.TICKLEFT),
            'inout': ('_', '_'),
        }[self._tickdir]
        self.stale = True
