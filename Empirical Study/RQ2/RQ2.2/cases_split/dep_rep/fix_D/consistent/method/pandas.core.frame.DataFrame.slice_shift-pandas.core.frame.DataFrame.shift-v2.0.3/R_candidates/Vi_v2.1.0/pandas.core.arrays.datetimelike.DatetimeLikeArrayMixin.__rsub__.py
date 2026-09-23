    def __rsub__(self, other):
        other_dtype = getattr(other, "dtype", None)
        other_is_dt64 = lib.is_np_dtype(other_dtype, "M") or isinstance(
            other_dtype, DatetimeTZDtype
        )

        if other_is_dt64 and lib.is_np_dtype(self.dtype, "m"):
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
        elif self.dtype.kind == "M" and hasattr(other, "dtype") and not other_is_dt64:
            # GH#19959 datetime - datetime is well-defined as timedelta,
            # but any other type - datetime is not well-defined.
            raise TypeError(
                f"cannot subtract {type(self).__name__} from {type(other).__name__}"
            )
        elif isinstance(self.dtype, PeriodDtype) and lib.is_np_dtype(other_dtype, "m"):
            # TODO: Can we simplify/generalize these cases at all?
            raise TypeError(f"cannot subtract {type(self).__name__} from {other.dtype}")
        elif lib.is_np_dtype(self.dtype, "m"):
            self = cast("TimedeltaArray", self)
            return (-self) + other

        # We get here with e.g. datetime objects
        return -(self - other)
