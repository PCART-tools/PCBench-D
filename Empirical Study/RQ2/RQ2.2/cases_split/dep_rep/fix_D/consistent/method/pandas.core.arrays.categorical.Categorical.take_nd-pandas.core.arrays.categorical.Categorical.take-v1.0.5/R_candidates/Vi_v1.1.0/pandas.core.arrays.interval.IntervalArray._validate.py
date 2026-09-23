    def _validate(self):
        """
        Verify that the IntervalArray is valid.

        Checks that

        * closed is valid
        * left and right match lengths
        * left and right have the same missing values
        * left is always below right
        """
        if self.closed not in _VALID_CLOSED:
            msg = f"invalid option for 'closed': {self.closed}"
            raise ValueError(msg)
        if len(self.left) != len(self.right):
            msg = "left and right must have the same length"
            raise ValueError(msg)
        left_mask = notna(self.left)
        right_mask = notna(self.right)
        if not (left_mask == right_mask).all():
            msg = (
                "missing values must be missing in the same "
                "location both left and right sides"
            )
            raise ValueError(msg)
        if not (self.left[left_mask] <= self.right[left_mask]).all():
            msg = "left side of interval must be <= right side"
            raise ValueError(msg)
