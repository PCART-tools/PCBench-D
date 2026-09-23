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
                warnings.warn(
                    "In a future version, passing a SparseArray to pd.Index "
                    "will store that array directly instead of converting to a "
                    "dense numpy ndarray. To retain the old behavior, use "
                    "pd.Index(arr.to_numpy()) instead",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
                return cls._dtype_to_subclass(dtype.subtype)

            return Index

        if dtype.kind == "M":
            from pandas import DatetimeIndex

            return DatetimeIndex

        elif dtype.kind == "m":
            from pandas import TimedeltaIndex

            return TimedeltaIndex

        elif is_float_dtype(dtype):
            from pandas.core.api import Float64Index

            return Float64Index
        elif is_unsigned_integer_dtype(dtype):
            from pandas.core.api import UInt64Index

            return UInt64Index
        elif is_signed_integer_dtype(dtype):
            from pandas.core.api import Int64Index

            return Int64Index

        elif dtype == _dtype_obj:
            # NB: assuming away MultiIndex
            return Index

        elif issubclass(dtype.type, (str, bool, np.bool_)):
            return Index

        raise NotImplementedError(dtype)
