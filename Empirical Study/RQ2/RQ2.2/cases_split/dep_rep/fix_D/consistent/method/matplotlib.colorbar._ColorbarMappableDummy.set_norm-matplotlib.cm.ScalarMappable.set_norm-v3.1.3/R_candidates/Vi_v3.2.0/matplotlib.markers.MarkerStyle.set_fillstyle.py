    def set_fillstyle(self, fillstyle):
        """
        Sets fillstyle

        Parameters
        ----------
        fillstyle : string amongst known fillstyles
        """
        if fillstyle is None:
            fillstyle = rcParams['markers.fillstyle']
        cbook._check_in_list(self.fillstyles, fillstyle=fillstyle)
        self._fillstyle = fillstyle
        self._recache()
