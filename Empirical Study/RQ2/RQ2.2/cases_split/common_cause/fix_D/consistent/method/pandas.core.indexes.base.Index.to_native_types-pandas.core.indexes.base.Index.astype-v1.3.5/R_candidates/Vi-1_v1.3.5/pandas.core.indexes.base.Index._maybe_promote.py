    @final
    def _maybe_promote(self, other: Index) -> tuple[Index, Index]:
        """
        When dealing with an object-dtype Index and a non-object Index, see
        if we can upcast the object-dtype one to improve performance.
        """

        if isinstance(self, ABCDatetimeIndex) and isinstance(other, ABCDatetimeIndex):
            if (
                self.tz is not None
                and other.tz is not None
                and not tz_compare(self.tz, other.tz)
            ):
                # standardize on UTC
                return self.tz_convert("UTC"), other.tz_convert("UTC")

        elif self.inferred_type == "date" and isinstance(other, ABCDatetimeIndex):
            try:
                return type(other)(self), other
            except OutOfBoundsDatetime:
                return self, other
        elif self.inferred_type == "timedelta" and isinstance(other, ABCTimedeltaIndex):
            # TODO: we dont have tests that get here
            return type(other)(self), other
        elif self.inferred_type == "boolean":
            if not is_object_dtype(self.dtype):
                return self.astype("object"), other.astype("object")

        elif self.dtype.kind == "u" and other.dtype.kind == "i":
            # GH#41873
            if other.min() >= 0:
                # lookup min as it may be cached
                # TODO: may need itemsize check if we have non-64-bit Indexes
                return self, other.astype(self.dtype)

        if not is_object_dtype(self.dtype) and is_object_dtype(other.dtype):
            # Reverse op so we dont need to re-implement on the subclasses
            other, self = other._maybe_promote(self)

        return self, other
