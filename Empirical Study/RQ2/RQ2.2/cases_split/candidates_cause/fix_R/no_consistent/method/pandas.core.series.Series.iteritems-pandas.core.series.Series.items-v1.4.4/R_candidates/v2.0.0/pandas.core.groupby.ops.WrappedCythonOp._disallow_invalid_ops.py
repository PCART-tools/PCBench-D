    def _disallow_invalid_ops(self, dtype: DtypeObj, is_numeric: bool = False):
        """
        Check if we can do this operation with our cython functions.

        Raises
        ------
        TypeError
            This is not a valid operation for this dtype.
        NotImplementedError
            This may be a valid operation, but does not have a cython implementation.
        """
        how = self.how

        if is_numeric:
            # never an invalid op for those dtypes, so return early as fastpath
            return

        if isinstance(dtype, CategoricalDtype):
            if how in ["sum", "prod", "cumsum", "cumprod"]:
                raise TypeError(f"{dtype} type does not support {how} operations")
            if how in ["min", "max", "rank"] and not dtype.ordered:
                # raise TypeError instead of NotImplementedError to ensure we
                #  don't go down a group-by-group path, since in the empty-groups
                #  case that would fail to raise
                raise TypeError(f"Cannot perform {how} with non-ordered Categorical")
            if how not in ["rank"]:
                # only "rank" is implemented in cython
                raise NotImplementedError(f"{dtype} dtype not supported")

        elif is_sparse(dtype):
            raise NotImplementedError(f"{dtype} dtype not supported")
        elif is_datetime64_any_dtype(dtype):
            # Adding/multiplying datetimes is not valid
            if how in ["sum", "prod", "cumsum", "cumprod"]:
                raise TypeError(f"datetime64 type does not support {how} operations")
        elif is_period_dtype(dtype):
            # Adding/multiplying Periods is not valid
            if how in ["sum", "prod", "cumsum", "cumprod"]:
                raise TypeError(f"Period type does not support {how} operations")
        elif is_timedelta64_dtype(dtype):
            # timedeltas we can add but not multiply
            if how in ["prod", "cumprod"]:
                raise TypeError(f"timedelta64 type does not support {how} operations")
