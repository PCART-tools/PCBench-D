    def set_ticks_position(self, position):
        """
        Set the ticks position.

        Parameters
        ----------
        position : {'top', 'bottom', 'both', 'default', 'none'}
            'both' sets the ticks to appear on both positions, but does not
            change the tick labels.  'default' resets the tick positions to
            the default: ticks on both positions, labels at bottom.  'none'
            can be used if you don't want any ticks. 'none' and 'both'
            affect only the ticks, not the labels.
        """
        if position == 'top':
            self.set_tick_params(which='both', top=True, labeltop=True,
                                 bottom=False, labelbottom=False)
            self._tick_position = 'top'
            self.offsetText.set_verticalalignment('bottom')
        elif position == 'bottom':
            self.set_tick_params(which='both', top=False, labeltop=False,
                                 bottom=True, labelbottom=True)
            self._tick_position = 'bottom'
            self.offsetText.set_verticalalignment('top')
        elif position == 'both':
            self.set_tick_params(which='both', top=True,
                                 bottom=True)
        elif position == 'none':
            self.set_tick_params(which='both', top=False,
                                 bottom=False)
        elif position == 'default':
            self.set_tick_params(which='both', top=True, labeltop=False,
                                 bottom=True, labelbottom=True)
            self._tick_position = 'bottom'
            self.offsetText.set_verticalalignment('top')
        else:
            _api.check_in_list(['top', 'bottom', 'both', 'default', 'none'],
                               position=position)
        self.stale = True
