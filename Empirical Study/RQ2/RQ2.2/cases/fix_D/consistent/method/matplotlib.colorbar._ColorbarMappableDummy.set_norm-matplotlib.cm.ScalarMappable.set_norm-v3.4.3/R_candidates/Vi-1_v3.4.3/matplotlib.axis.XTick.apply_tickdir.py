    def apply_tickdir(self, tickdir):
        # docstring inherited
        super().apply_tickdir(tickdir)
        self._tickmarkers = {
            'out': (mlines.TICKDOWN, mlines.TICKUP),
            'in': (mlines.TICKUP, mlines.TICKDOWN),
            'inout': ('|', '|'),
        }[self._tickdir]
        self.stale = True
