    def tick_bottom(self):
        """
        Move ticks and ticklabels (if present) to the bottom of the axes.
        """
        label = True
        if 'label1On' in self._major_tick_kw:
            label = (self._major_tick_kw['label1On']
                     or self._major_tick_kw['label2On'])
        self.set_ticks_position('bottom')
        # If labels were turned off before this was called, leave them off.
        self.set_tick_params(which='both', labelbottom=label)
