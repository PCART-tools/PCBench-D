    @classmethod
    def _validate(cls, left, right, dtype: IntervalDtype) -> None:
        """
        Verify that the IntervalArray is valid.

        Checks that

        * dtype is correct
        * left and right match lengths
        * left and right have the same missing values
        * left is always below right
        """
        if not isinstance(dtype, IntervalDtype):
            msg = f"invalid dtype: {dtype}"
            raise ValueError(msg)
        if len(left) != len(right):
            msg = "left and right must have the same length"
            raise ValueError(msg)
        left_mask = notna(left)
        right_mask = notna(right)
        if not (left_mask == right_mask).all():
            msg = (
                "missing values must be missing in the same "
                "location both left and right sides"
            )
            raise ValueError(msg)
        if not (left[left_mask] <= right[left_mask]).all():
            msg = "left side of interval must be <= right side"
            raise ValueError(msg)
