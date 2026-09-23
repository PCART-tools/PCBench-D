    def delete(self: _IndexT, loc) -> _IndexT:
        """
        Make new Index with passed location(-s) deleted.

        Parameters
        ----------
        loc : int or list of int
            Location of item(-s) which will be deleted.
            Use a list of locations to delete more than one value at the same time.

        Returns
        -------
        Index
            Will be same type as self, except for RangeIndex.

        See Also
        --------
        numpy.delete : Delete any rows and column from NumPy array (ndarray).

        Examples
        --------
        >>> idx = pd.Index(['a', 'b', 'c'])
        >>> idx.delete(1)
        Index(['a', 'c'], dtype='object')

        >>> idx = pd.Index(['a', 'b', 'c'])
        >>> idx.delete([0, 2])
        Index(['b'], dtype='object')
        """
        values = self._values
        res_values: ArrayLike
        if isinstance(values, np.ndarray):
            # TODO(__array_function__): special casing will be unnecessary
            res_values = np.delete(values, loc)
        else:
            res_values = values.delete(loc)

        # _constructor so RangeIndex->Int64Index
        return self._constructor._simple_new(res_values, name=self.name)
