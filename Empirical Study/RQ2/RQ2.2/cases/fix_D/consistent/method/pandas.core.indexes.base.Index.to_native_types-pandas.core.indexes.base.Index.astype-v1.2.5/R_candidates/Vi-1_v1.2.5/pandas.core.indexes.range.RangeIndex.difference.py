    def difference(self, other, sort=None):
        # optimized set operation if we have another RangeIndex
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, result_name = self._convert_can_do_setop(other)

        if not isinstance(other, RangeIndex):
            return super().difference(other, sort=sort)

        res_name = ops.get_op_result_name(self, other)

        first = self._range[::-1] if self.step < 0 else self._range
        overlap = self.intersection(other)
        if overlap.step < 0:
            overlap = overlap[::-1]

        if len(overlap) == 0:
            return self._shallow_copy(name=res_name)
        if len(overlap) == len(self):
            return self[:0].rename(res_name)
        if not isinstance(overlap, RangeIndex):
            # We wont end up with RangeIndex, so fall back
            return super().difference(other, sort=sort)
        if overlap.step != first.step:
            # In some cases we might be able to get a RangeIndex back,
            #  but not worth the effort.
            return super().difference(other, sort=sort)

        if overlap[0] == first.start:
            # The difference is everything after the intersection
            new_rng = range(overlap[-1] + first.step, first.stop, first.step)
        elif overlap[-1] == first[-1]:
            # The difference is everything before the intersection
            new_rng = range(first.start, overlap[0], first.step)
        else:
            # The difference is not range-like
            return super().difference(other, sort=sort)

        new_index = type(self)._simple_new(new_rng, name=res_name)
        if first is not self._range:
            new_index = new_index[::-1]
        return new_index
