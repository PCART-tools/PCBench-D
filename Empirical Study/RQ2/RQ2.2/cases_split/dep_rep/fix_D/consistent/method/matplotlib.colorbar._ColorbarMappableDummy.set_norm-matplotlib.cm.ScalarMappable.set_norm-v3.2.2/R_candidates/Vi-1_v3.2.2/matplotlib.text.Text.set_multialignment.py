    def set_multialignment(self, align):
        """
        Set the alignment for multiple lines layout.  The layout of the
        bounding box of all the lines is determined by the horizontalalignment
        and verticalalignment properties, but the multiline text within that
        box can be

        Parameters
        ----------
        align : {'left', 'right', 'center'}
        """
        cbook._check_in_list(['center', 'right', 'left'], align=align)
        self._multialignment = align
        self.stale = True
