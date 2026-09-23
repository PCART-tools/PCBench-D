    def asof_locs(self, where, mask):
        """
        Finds the locations (indices) of the labels from the index for
        every entry in the `where` argument.

        As in the `asof` function, if the label (a particular entry in
        `where`) is not in the index, the latest index label upto the
        passed label is chosen and its index returned.

        If all of the labels in the index are later than a label in `where`,
        -1 is returned.

        `mask` is used to ignore NA values in the index during calculation.

        Parameters
        ----------
        where : Index
            An Index consisting of an array of timestamps.
        mask : array-like
            Array of booleans denoting where values in the original
            data are not NA.

        Returns
        -------
        numpy.ndarray
            An array of locations (indices) of the labels from the Index
            which correspond to the return values of the `asof` function
            for every element in `where`.
        """
        locs = self.values[mask].searchsorted(where.values, side='right')
        locs = np.where(locs > 0, locs - 1, 0)

        result = np.arange(len(self))[mask].take(locs)

        first = mask.argmax()
        result[(locs == 0) & (where.values < self.values[first])] = -1

        return result
