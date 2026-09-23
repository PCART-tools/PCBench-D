    def _is_compatible_with_other(self, other):
        return super()._is_compatible_with_other(other) or all(
            isinstance(
                type(obj),
                (ABCInt64Index, ABCFloat64Index, ABCUInt64Index, ABCRangeIndex),
            )
            for obj in [self, other]
        )
