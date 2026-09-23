    def tick_top(self):
        """
        Move ticks and ticklabels (if present) to the top of the axes.
        """
        label = True
        if 'label1On' in self._major_tick_kw:
            label = (self._major_tick_kw['label1On']
                     or self._major_tick_kw['label2On'])
        self.set_ticks_position('top')
        # if labels were turned off before this was called
        # leave them off
        self.set_tick_params(which='both', labeltop=label)
