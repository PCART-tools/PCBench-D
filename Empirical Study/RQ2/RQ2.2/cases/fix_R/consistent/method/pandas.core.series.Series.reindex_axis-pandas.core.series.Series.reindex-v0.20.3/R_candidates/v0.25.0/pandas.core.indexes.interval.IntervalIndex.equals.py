    def equals(self, other):
        """
        Determines if two IntervalIndex objects contain the same elements
        """
        if self.is_(other):
            return True

        # if we can coerce to an II
        # then we can compare
        if not isinstance(other, IntervalIndex):
            if not is_interval_dtype(other):
                return False
            other = Index(getattr(other, ".values", other))

        return (
            self.left.equals(other.left)
            and self.right.equals(other.right)
            and self.closed == other.closed
        )
