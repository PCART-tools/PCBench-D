    def set_verticalalignment(self, align):
        """
        Set the vertical alignment

        ACCEPTS: [ 'center' | 'top' | 'bottom' | 'baseline' ]
        """
        legal = ('top', 'bottom', 'center', 'baseline')
        if align not in legal:
            raise ValueError('Vertical alignment must be one of %s' %
                             str(legal))

        self._verticalalignment = align
        self.stale = True
