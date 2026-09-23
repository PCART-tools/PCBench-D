    def head(self, n=5):
        """
        Return the first n rows.

        Parameters
        ----------
        n : int, default 5
            Number of rows to select.

        Returns
        -------
        obj_head : type of caller
            The first n rows of the caller object.
        """

        return self.iloc[:n]
