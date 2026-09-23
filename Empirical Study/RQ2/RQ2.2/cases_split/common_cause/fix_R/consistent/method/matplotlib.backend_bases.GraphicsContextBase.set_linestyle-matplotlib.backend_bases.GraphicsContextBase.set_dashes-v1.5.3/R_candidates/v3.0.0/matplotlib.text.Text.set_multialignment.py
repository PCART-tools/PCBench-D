    def set_multialignment(self, align):
        """
        Set the alignment for multiple lines layout.  The layout of the
        bounding box of all the lines is determined bu the horizontalalignment
        and verticalalignment properties, but the multiline text within that
        box can be

        Parameters
        ----------
        align : {'left', 'right', 'center'}
        """
        legal = ('center', 'right', 'left')
        if align not in legal:
            raise ValueError('Horizontal alignment must be one of %s' %
                             str(legal))
        self._multialignment = align
        self.stale = True
