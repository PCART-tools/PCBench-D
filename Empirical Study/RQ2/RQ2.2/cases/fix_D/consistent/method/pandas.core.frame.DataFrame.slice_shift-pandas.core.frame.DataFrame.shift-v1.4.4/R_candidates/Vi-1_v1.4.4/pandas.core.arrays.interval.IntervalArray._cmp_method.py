    def _cmp_method(self, other, op):
        # ensure pandas array for list-like and eliminate non-interval scalars
        if is_list_like(other):
            if len(self) != len(other):
                raise ValueError("Lengths must match to compare")
            other = pd_array(other)
        elif not isinstance(other, Interval):
            # non-interval scalar -> no matches
            if other is NA:
                # GH#31882
                from pandas.core.arrays import BooleanArray

                arr = np.empty(self.shape, dtype=bool)
                mask = np.ones(self.shape, dtype=bool)
                return BooleanArray(arr, mask)
            return invalid_comparison(self, other, op)

        # determine the dtype of the elements we want to compare
        if isinstance(other, Interval):
            other_dtype = pandas_dtype("interval")
        elif not is_categorical_dtype(other.dtype):
            other_dtype = other.dtype
        else:
            # for categorical defer to categories for dtype
            other_dtype = other.categories.dtype

            # extract intervals if we have interval categories with matching closed
            if is_interval_dtype(other_dtype):
                if self.closed != other.categories.closed:
                    return invalid_comparison(self, other, op)

                other = other.categories.take(
                    other.codes, allow_fill=True, fill_value=other.categories._na_value
                )

        # interval-like -> need same closed and matching endpoints
        if is_interval_dtype(other_dtype):
            if self.closed != other.closed:
                return invalid_comparison(self, other, op)
            elif not isinstance(other, Interval):
                other = type(self)(other)

            if op is operator.eq:
                return (self._left == other.left) & (self._right == other.right)
            elif op is operator.ne:
                return (self._left != other.left) | (self._right != other.right)
            elif op is operator.gt:
                return (self._left > other.left) | (
                    (self._left == other.left) & (self._right > other.right)
                )
            elif op is operator.ge:
                return (self == other) | (self > other)
            elif op is operator.lt:
                return (self._left < other.left) | (
                    (self._left == other.left) & (self._right < other.right)
                )
            else:
                # operator.lt
                return (self == other) | (self < other)

        # non-interval/non-object dtype -> no matches
        if not is_object_dtype(other_dtype):
            return invalid_comparison(self, other, op)

        # object dtype -> iteratively check for intervals
        result = np.zeros(len(self), dtype=bool)
        for i, obj in enumerate(other):
            try:
                result[i] = op(self[i], obj)
            except TypeError:
                if obj is NA:
                    # comparison with np.nan returns NA
                    # github.com/pandas-dev/pandas/pull/37124#discussion_r509095092
                    result = result.astype(object)
                    result[i] = NA
                else:
                    raise
        return result
