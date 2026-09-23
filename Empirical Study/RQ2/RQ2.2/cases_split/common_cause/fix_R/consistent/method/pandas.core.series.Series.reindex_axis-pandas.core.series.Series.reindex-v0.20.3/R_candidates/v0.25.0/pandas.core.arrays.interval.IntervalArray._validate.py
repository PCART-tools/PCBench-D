    def _validate(self):
        """Verify that the IntervalArray is valid.

        Checks that

        * closed is valid
        * left and right match lengths
        * left and right have the same missing values
        * left is always below right
        """
        if self.closed not in _VALID_CLOSED:
            raise ValueError(
                "invalid option for 'closed': {closed}".format(closed=self.closed)
            )
        if len(self.left) != len(self.right):
            raise ValueError("left and right must have the same length")
        left_mask = notna(self.left)
        right_mask = notna(self.right)
        if not (left_mask == right_mask).all():
            raise ValueError(
                "missing values must be missing in the same "
                "location both left and right sides"
            )
        if not (self.left[left_mask] <= self.right[left_mask]).all():
            raise ValueError("left side of interval must be <= right side")
