    def diff(self, n: int, axis: int = 0) -> list[Block]:
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
        A list with a new Block.

        Notes
        -----
        The arguments here are mimicking shift so they are called correctly
        by apply.
        """
        values = self.values

        new_values = values - values.shift(n, axis=axis)
        return [self.make_block(new_values)]
