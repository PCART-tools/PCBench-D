    def apply_tickdir(self, tickdir):
        """Set tick direction.  Valid values are 'out', 'in', 'inout'."""
        if tickdir is None:
            tickdir = mpl.rcParams[f'{self.__name__}.direction']
        _api.check_in_list(['in', 'out', 'inout'], tickdir=tickdir)
        self._tickdir = tickdir
        self._pad = self._base_pad + self.get_tick_padding()
        self.stale = True
