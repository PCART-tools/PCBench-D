    def set_dashpad(self, dp):
        """
        Set the "pad" of the TextWithDash, which is the extra spacing
        between the dash and the text, in canvas units.

        Parameters
        ----------
        dp : float
        """
        self._dashpad = dp
        self.stale = True
