    def __rsub__(self, other):
        other_dtype = getattr(other, "dtype", None)

        if is_datetime64_any_dtype(other_dtype) and is_timedelta64_dtype(self.dtype):
            # ndarray[datetime64] cannot be subtracted from self, so
            # we need to wrap in DatetimeArray/Index and flip the operation
            if lib.is_scalar(other):
                # i.e. np.datetime64 object
                return Timestamp(other) - self
            if not isinstance(other, DatetimeLikeArrayMixin):
                # Avoid down-casting DatetimeIndex
                from pandas.core.arrays import DatetimeArray

                other = DatetimeArray(other)
            return other - self
        elif (
            is_datetime64_any_dtype(self.dtype)
            and hasattr(other, "dtype")
            and not is_datetime64_any_dtype(other.dtype)
        ):
            # GH#19959 datetime - datetime is well-defined as timedelta,
            # but any other type - datetime is not well-defined.
            raise TypeError(
                f"cannot subtract {type(self).__name__} from {type(other).__name__}"
            )
        elif is_period_dtype(self.dtype) and is_timedelta64_dtype(other_dtype):
            # TODO: Can we simplify/generalize these cases at all?
            raise TypeError(f"cannot subtract {type(self).__name__} from {other.dtype}")
        elif is_timedelta64_dtype(self.dtype):
            self = cast("TimedeltaArray", self)
            return (-self) + other

        # We get here with e.g. datetime objects
        return -(self - other)
