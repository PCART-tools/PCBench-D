    def set_dashpush(self, dp):
        """
        Set the "push" of the TextWithDash, which is the extra spacing between
        the beginning of the dash and the specified position.

        Parameters
        ----------
        dp : float
        """
        self._dashpush = dp
        self.stale = True
