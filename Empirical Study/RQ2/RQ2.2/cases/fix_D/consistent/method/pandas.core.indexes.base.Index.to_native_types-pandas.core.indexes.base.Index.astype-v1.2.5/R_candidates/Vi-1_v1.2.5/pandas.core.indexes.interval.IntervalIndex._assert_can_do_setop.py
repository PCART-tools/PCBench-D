    def _assert_can_do_setop(self, other):
        super()._assert_can_do_setop(other)

        if isinstance(other, IntervalIndex) and self._is_non_comparable_own_type(other):
            # GH#19016: ensure set op will not return a prohibited dtype
            raise TypeError(
                "can only do set operations between two IntervalIndex "
                "objects that are closed on the same side "
                "and have compatible dtypes"
            )
