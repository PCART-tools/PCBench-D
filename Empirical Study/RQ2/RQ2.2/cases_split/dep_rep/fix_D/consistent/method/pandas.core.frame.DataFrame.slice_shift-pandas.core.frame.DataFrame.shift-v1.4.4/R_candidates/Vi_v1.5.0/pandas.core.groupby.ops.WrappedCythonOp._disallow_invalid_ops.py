    def _disallow_invalid_ops(self, dtype: DtypeObj, is_numeric: bool = False):
        """
        Check if we can do this operation with our cython functions.

        Raises
        ------
        NotImplementedError
            This is either not a valid function for this dtype, or
            valid but not implemented in cython.
        """
        how = self.how

        if is_numeric:
            # never an invalid op for those dtypes, so return early as fastpath
            return

        if isinstance(dtype, CategoricalDtype):
            # NotImplementedError for methods that can fall back to a
            #  non-cython implementation.
            if how in ["sum", "prod", "cumsum", "cumprod"]:
                raise TypeError(f"{dtype} type does not support {how} operations")
            elif how not in ["rank"]:
                # only "rank" is implemented in cython
                raise NotImplementedError(f"{dtype} dtype not supported")
            elif not dtype.ordered:
                # TODO: TypeError?
                raise NotImplementedError(f"{dtype} dtype not supported")

        elif is_sparse(dtype):
            # categoricals are only 1d, so we
            #  are not setup for dim transforming
            raise NotImplementedError(f"{dtype} dtype not supported")
        elif is_datetime64_any_dtype(dtype):
            # TODO: same for period_dtype?  no for these methods with Period
            # we raise NotImplemented if this is an invalid operation
            #  entirely, e.g. adding datetimes
            if how in ["sum", "prod", "cumsum", "cumprod"]:
                raise TypeError(f"datetime64 type does not support {how} operations")
        elif is_timedelta64_dtype(dtype):
            if how in ["prod", "cumprod"]:
                raise TypeError(f"timedelta64 type does not support {how} operations")
