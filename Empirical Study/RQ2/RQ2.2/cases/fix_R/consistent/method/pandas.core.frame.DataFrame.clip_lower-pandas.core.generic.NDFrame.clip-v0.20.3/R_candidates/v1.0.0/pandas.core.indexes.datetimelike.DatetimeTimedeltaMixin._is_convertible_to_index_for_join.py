    @classmethod
    def _is_convertible_to_index_for_join(cls, other: Index) -> bool:
        """
        return a boolean whether I can attempt conversion to a
        DatetimeIndex/TimedeltaIndex
        """
        if isinstance(other, cls):
            return False
        elif len(other) > 0 and other.inferred_type not in (
            "floating",
            "mixed-integer",
            "integer",
            "integer-na",
            "mixed-integer-float",
            "mixed",
        ):
            return True
        return False
