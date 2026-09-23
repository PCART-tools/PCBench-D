    def set_horizontalalignment(self, align):
        """
        Set the horizontal alignment to one of

        ACCEPTS: [ 'center' | 'right' | 'left' ]
        """
        legal = ('center', 'right', 'left')
        if align not in legal:
            raise ValueError('Horizontal alignment must be one of %s' %
                             str(legal))
        self._horizontalalignment = align
        self.stale = True
