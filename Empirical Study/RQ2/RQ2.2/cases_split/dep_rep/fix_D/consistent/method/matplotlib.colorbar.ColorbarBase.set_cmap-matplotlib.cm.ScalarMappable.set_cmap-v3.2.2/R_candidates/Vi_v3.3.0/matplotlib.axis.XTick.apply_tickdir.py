    def apply_tickdir(self, tickdir):
        """Set tick direction. Valid values are 'in', 'out', 'inout'."""
        if tickdir is None:
            tickdir = mpl.rcParams['%s.direction' % self.__name__.lower()]
        cbook._check_in_list(['in', 'out', 'inout'], tickdir=tickdir)
        self._tickdir = tickdir

        if self._tickdir == 'in':
            self._tickmarkers = (mlines.TICKUP, mlines.TICKDOWN)
        elif self._tickdir == 'inout':
            self._tickmarkers = ('|', '|')
        else:
            self._tickmarkers = (mlines.TICKDOWN, mlines.TICKUP)
        self._pad = self._base_pad + self.get_tick_padding()
        self.stale = True
