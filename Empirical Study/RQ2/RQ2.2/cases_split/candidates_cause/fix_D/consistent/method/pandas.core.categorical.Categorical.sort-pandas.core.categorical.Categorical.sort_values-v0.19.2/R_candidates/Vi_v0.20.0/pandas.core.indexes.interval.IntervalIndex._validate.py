    def _validate(self):
        """
        Verify that the IntervalIndex is valid.
        """
        if self.closed not in _VALID_CLOSED:
            raise ValueError("invalid options for 'closed': %s" % self.closed)
        if len(self.left) != len(self.right):
            raise ValueError('left and right must have the same length')
        left_mask = notnull(self.left)
        right_mask = notnull(self.right)
        if not (left_mask == right_mask).all():
            raise ValueError('missing values must be missing in the same '
                             'location both left and right sides')
        if not (self.left[left_mask] <= self.right[left_mask]).all():
            raise ValueError('left side of interval must be <= right side')
        self._mask = ~left_mask
