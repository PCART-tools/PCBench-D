    def mode(self):
        """Return the mode(s) of the dataset.

        Always returns Series even if only one value is returned.

        Returns
        -------
        modes : Series (sorted)
        """
        # TODO: Add option for bins like value_counts()
        return algorithms.mode(self)
