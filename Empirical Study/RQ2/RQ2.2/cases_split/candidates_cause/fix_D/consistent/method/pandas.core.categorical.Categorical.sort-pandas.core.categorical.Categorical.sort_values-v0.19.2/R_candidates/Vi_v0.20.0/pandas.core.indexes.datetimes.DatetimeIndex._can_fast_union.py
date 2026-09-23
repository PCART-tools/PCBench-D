    def _can_fast_union(self, other):
        if not isinstance(other, DatetimeIndex):
            return False

        offset = self.offset

        if offset is None or offset != other.offset:
            return False

        if not self.is_monotonic or not other.is_monotonic:
            return False

        if len(self) == 0 or len(other) == 0:
            return True

        # to make our life easier, "sort" the two ranges
        if self[0] <= other[0]:
            left, right = self, other
        else:
            left, right = other, self

        right_start = right[0]
        left_end = left[-1]

        # Only need to "adjoin", not overlap
        try:
            return (right_start == left_end + offset) or right_start in left
        except (ValueError):

            # if we are comparing an offset that does not propagate timezones
            # this will raise
            return False
