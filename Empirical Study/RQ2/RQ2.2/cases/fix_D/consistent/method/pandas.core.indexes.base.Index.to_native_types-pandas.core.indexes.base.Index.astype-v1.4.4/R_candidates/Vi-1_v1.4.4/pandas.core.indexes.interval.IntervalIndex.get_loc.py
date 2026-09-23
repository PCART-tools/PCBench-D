    def get_loc(
        self, key, method: str | None = None, tolerance=None
    ) -> int | slice | np.ndarray:
        """
        Get integer location, slice or boolean mask for requested label.

        Parameters
        ----------
        key : label
        method : {None}, optional
            * default: matches where the label is within an interval only.

        Returns
        -------
        int if unique index, slice if monotonic index, else mask

        Examples
        --------
        >>> i1, i2 = pd.Interval(0, 1), pd.Interval(1, 2)
        >>> index = pd.IntervalIndex([i1, i2])
        >>> index.get_loc(1)
        0

        You can also supply a point inside an interval.

        >>> index.get_loc(1.5)
        1

        If a label is in several intervals, you get the locations of all the
        relevant intervals.

        >>> i3 = pd.Interval(0, 2)
        >>> overlapping_index = pd.IntervalIndex([i1, i2, i3])
        >>> overlapping_index.get_loc(0.5)
        array([ True, False,  True])

        Only exact matches will be returned if an interval is provided.

        >>> index.get_loc(pd.Interval(0, 1))
        0
        """
        self._check_indexing_method(method)
        self._check_indexing_error(key)

        if isinstance(key, Interval):
            if self.closed != key.closed:
                raise KeyError(key)
            mask = (self.left == key.left) & (self.right == key.right)
        elif is_valid_na_for_dtype(key, self.dtype):
            mask = self.isna()
        else:
            # assume scalar
            op_left = le if self.closed_left else lt
            op_right = le if self.closed_right else lt
            try:
                mask = op_left(self.left, key) & op_right(key, self.right)
            except TypeError as err:
                # scalar is not comparable to II subtype --> invalid label
                raise KeyError(key) from err

        matches = mask.sum()
        if matches == 0:
            raise KeyError(key)
        elif matches == 1:
            return mask.argmax()

        res = lib.maybe_booleans_to_slice(mask.view("u1"))
        if isinstance(res, slice) and res.stop is None:
            # TODO: DO this in maybe_booleans_to_slice?
            res = slice(res.start, len(self), res.step)
        return res
