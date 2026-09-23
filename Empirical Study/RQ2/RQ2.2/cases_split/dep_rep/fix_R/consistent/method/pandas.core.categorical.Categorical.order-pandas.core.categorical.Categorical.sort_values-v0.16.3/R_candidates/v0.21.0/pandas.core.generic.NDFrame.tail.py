    def tail(self, n=5):
        """
        Return the last n rows.

        Parameters
        ----------
        n : int, default 5
            Number of rows to select.

        Returns
        -------
        obj_tail : type of caller
            The last n rows of the caller object.
        """

        if n == 0:
            return self.iloc[0:0]
        return self.iloc[-n:]
