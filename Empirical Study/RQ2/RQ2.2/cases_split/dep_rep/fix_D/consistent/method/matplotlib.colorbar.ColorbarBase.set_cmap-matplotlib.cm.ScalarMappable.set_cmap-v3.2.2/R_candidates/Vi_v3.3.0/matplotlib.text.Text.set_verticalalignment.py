    def set_verticalalignment(self, align):
        """
        Set the vertical alignment.

        Parameters
        ----------
        align : {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
        """
        cbook._check_in_list(
            ['top', 'bottom', 'center', 'baseline', 'center_baseline'],
            align=align)
        self._verticalalignment = align
        self.stale = True
