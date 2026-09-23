    def set_horizontalalignment(self, align):
        """
        Set the horizontal alignment to one of

        Parameters
        ----------
        align : {'center', 'right', 'left'}
        """
        _api.check_in_list(['center', 'right', 'left'], align=align)
        self._horizontalalignment = align
        self.stale = True
