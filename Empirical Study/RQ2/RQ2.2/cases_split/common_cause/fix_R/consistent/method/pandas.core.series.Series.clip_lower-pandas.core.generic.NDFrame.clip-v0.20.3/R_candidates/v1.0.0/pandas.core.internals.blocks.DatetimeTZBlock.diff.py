    def diff(self, n: int, axis: int = 0) -> List["Block"]:
        """
        1st discrete difference.

        Parameters
        ----------
        n : int
            Number of periods to diff.
        axis : int, default 0
            Axis to diff upon.

        Returns
        -------
        A list with a new TimeDeltaBlock.

        Notes
        -----
        The arguments here are mimicking shift so they are called correctly
        by apply.
        """
        if axis == 0:
            # Cannot currently calculate diff across multiple blocks since this
            # function is invoked via apply
            raise NotImplementedError
        new_values = (self.values - self.shift(n, axis=axis)[0].values).asi8

        # Reshape the new_values like how algos.diff does for timedelta data
        new_values = new_values.reshape(1, len(new_values))
        new_values = new_values.astype("timedelta64[ns]")
        return [TimeDeltaBlock(new_values, placement=self.mgr_locs.indexer)]
