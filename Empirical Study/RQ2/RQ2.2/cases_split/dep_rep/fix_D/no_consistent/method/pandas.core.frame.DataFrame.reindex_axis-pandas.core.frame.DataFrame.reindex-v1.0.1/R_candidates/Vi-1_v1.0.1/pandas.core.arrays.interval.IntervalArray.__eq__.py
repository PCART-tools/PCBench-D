    def __eq__(self, other):
        # ensure pandas array for list-like and eliminate non-interval scalars
        if is_list_like(other):
            if len(self) != len(other):
                raise ValueError("Lengths must match to compare")
            other = array(other)
        elif not isinstance(other, Interval):
            # non-interval scalar -> no matches
            return np.zeros(len(self), dtype=bool)

        # determine the dtype of the elements we want to compare
        if isinstance(other, Interval):
            other_dtype = "interval"
        elif not is_categorical_dtype(other):
            other_dtype = other.dtype
        else:
            # for categorical defer to categories for dtype
            other_dtype = other.categories.dtype

            # extract intervals if we have interval categories with matching closed
            if is_interval_dtype(other_dtype):
                if self.closed != other.categories.closed:
                    return np.zeros(len(self), dtype=bool)
                other = other.categories.take(other.codes)

        # interval-like -> need same closed and matching endpoints
        if is_interval_dtype(other_dtype):
            if self.closed != other.closed:
                return np.zeros(len(self), dtype=bool)
            return (self.left == other.left) & (self.right == other.right)

        # non-interval/non-object dtype -> no matches
        if not is_object_dtype(other_dtype):
            return np.zeros(len(self), dtype=bool)

        # object dtype -> iteratively check for intervals
        result = np.zeros(len(self), dtype=bool)
        for i, obj in enumerate(other):
            # need object to be an Interval with same closed and endpoints
            if (
                isinstance(obj, Interval)
                and self.closed == obj.closed
                and self.left[i] == obj.left
                and self.right[i] == obj.right
            ):
                result[i] = True

        return result
