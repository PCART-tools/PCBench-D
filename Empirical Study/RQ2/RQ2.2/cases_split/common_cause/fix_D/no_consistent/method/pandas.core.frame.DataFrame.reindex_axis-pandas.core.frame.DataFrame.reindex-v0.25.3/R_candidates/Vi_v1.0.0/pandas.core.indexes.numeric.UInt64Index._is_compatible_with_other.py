    def _is_compatible_with_other(self, other):
        return super()._is_compatible_with_other(other) or all(
            isinstance(type(obj), (ABCUInt64Index, ABCFloat64Index))
            for obj in [self, other]
        )
