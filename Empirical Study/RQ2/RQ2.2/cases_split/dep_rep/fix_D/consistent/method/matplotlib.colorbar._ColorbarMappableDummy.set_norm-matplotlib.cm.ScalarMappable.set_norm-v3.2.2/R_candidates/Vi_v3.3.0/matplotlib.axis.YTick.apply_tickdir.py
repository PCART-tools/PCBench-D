    def apply_tickdir(self, tickdir):
        if tickdir is None:
            tickdir = mpl.rcParams['%s.direction' % self.__name__.lower()]
        self._tickdir = tickdir

        if self._tickdir == 'in':
            self._tickmarkers = (mlines.TICKRIGHT, mlines.TICKLEFT)
        elif self._tickdir == 'inout':
            self._tickmarkers = ('_', '_')
        else:
            self._tickmarkers = (mlines.TICKLEFT, mlines.TICKRIGHT)
        self._pad = self._base_pad + self.get_tick_padding()
        self.stale = True
