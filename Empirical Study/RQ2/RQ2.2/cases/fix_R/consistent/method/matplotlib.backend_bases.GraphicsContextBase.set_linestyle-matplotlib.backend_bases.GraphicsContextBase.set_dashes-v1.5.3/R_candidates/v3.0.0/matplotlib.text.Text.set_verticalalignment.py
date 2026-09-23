    def set_verticalalignment(self, align):
        """
        Set the vertical alignment

        Parameters
        ----------
        align : {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
        """
        legal = ('top', 'bottom', 'center', 'baseline', 'center_baseline')
        if align not in legal:
            raise ValueError('Vertical alignment must be one of %s' %
                             str(legal))

        self._verticalalignment = align
        self.stale = True
