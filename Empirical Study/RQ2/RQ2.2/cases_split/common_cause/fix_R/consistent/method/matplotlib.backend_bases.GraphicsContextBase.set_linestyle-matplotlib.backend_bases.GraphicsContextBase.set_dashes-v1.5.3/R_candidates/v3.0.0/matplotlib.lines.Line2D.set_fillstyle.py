    def set_fillstyle(self, fs):
        """
        Set the marker fill style; 'full' means fill the whole marker.
        'none' means no filling; other options are for half-filled markers.

        Parameters
        ----------
        fs : {'full', 'left', 'right', 'bottom', 'top', 'none'}
        """
        self._marker.set_fillstyle(fs)
        self.stale = True
