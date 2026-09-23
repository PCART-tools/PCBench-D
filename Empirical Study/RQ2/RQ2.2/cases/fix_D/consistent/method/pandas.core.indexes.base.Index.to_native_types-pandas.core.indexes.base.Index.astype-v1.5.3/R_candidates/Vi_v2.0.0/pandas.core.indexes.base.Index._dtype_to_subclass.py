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

            return Index

        if dtype.kind == "M":
            from pandas import DatetimeIndex

            return DatetimeIndex

        elif dtype.kind == "m":
            from pandas import TimedeltaIndex

            return TimedeltaIndex

        elif dtype.kind == "O":
            # NB: assuming away MultiIndex
            return Index

        elif issubclass(dtype.type, str) or is_numeric_dtype(dtype):
            return Index

        raise NotImplementedError(dtype)
