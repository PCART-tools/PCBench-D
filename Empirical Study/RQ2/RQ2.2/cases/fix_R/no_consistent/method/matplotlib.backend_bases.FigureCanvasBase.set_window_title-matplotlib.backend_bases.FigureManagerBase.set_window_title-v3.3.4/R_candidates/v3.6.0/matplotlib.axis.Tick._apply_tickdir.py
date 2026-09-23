    def _apply_tickdir(self, tickdir):
        """Set tick direction.  Valid values are 'out', 'in', 'inout'."""
        # This method is responsible for updating `_pad`, and, in subclasses,
        # for setting the tick{1,2}line markers as well.  From the user
        # perspective this should always be called though _apply_params, which
        # further updates ticklabel positions using the new pads.
        if tickdir is None:
            tickdir = mpl.rcParams[f'{self.__name__}.direction']
        _api.check_in_list(['in', 'out', 'inout'], tickdir=tickdir)
        self._tickdir = tickdir
        self._pad = self._base_pad + self.get_tick_padding()
