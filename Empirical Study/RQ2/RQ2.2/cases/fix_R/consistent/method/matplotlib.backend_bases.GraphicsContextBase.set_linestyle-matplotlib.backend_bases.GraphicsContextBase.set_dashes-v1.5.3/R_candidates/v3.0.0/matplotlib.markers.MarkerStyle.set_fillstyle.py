    def set_fillstyle(self, fillstyle):
        """
        Sets fillstyle

        Parameters
        ----------
        fillstyle : string amongst known fillstyles
        """
        if fillstyle is None:
            fillstyle = rcParams['markers.fillstyle']
        if fillstyle not in self.fillstyles:
            raise ValueError("Unrecognized fillstyle %s"
                             % ' '.join(self.fillstyles))
        self._fillstyle = fillstyle
        self._recache()
