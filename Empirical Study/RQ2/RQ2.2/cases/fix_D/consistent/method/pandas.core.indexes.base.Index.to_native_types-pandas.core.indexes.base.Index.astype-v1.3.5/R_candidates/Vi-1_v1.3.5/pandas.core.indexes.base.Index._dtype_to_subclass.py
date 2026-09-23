    @final
    @classmethod
    def _dtype_to_subclass(cls, dtype: DtypeObj):
        # Delay import for perf. https://github.com/pandas-dev/pandas/pull/31423

        if isinstance(dtype, ExtensionDtype):
            if isinstance(dtype, DatetimeTZDtype):
                from pandas import DatetimeIndex

                return DatetimeIndex
            elif isinstance(dtype, CategoricalDtype):
                from pandas import CategoricalIndex

                return CategoricalIndex
            elif isinstance(dtype, IntervalDtype):
                from pandas import IntervalIndex

                return IntervalIndex
            elif isinstance(dtype, PeriodDtype):
                from pandas import PeriodIndex

                return PeriodIndex

            elif isinstance(dtype, SparseDtype):
                return cls._dtype_to_subclass(dtype.subtype)

            return Index

        if dtype.kind == "M":
            from pandas import DatetimeIndex

            return DatetimeIndex

        elif dtype.kind == "m":
            from pandas import TimedeltaIndex

            return TimedeltaIndex

        elif is_float_dtype(dtype):
            from pandas import Float64Index

            return Float64Index
        elif is_unsigned_integer_dtype(dtype):
            from pandas import UInt64Index

            return UInt64Index
        elif is_signed_integer_dtype(dtype):
            from pandas import Int64Index

            return Int64Index

        # error: Non-overlapping equality check (left operand type: "dtype[Any]", right
        # operand type: "Type[object]")
        elif dtype == object:  # type: ignore[comparison-overlap]
            # NB: assuming away MultiIndex
            return Index

        elif issubclass(dtype.type, (str, bool, np.bool_)):
            return Index

        raise NotImplementedError(dtype)
