    def _apply_tickdir(self, tickdir):
        # docstring inherited
        super()._apply_tickdir(tickdir)
        mark1, mark2 = _MARKER_DICT[self._tickdir]
        self.tick1line.set_marker(mark1)
        self.tick2line.set_marker(mark2)
