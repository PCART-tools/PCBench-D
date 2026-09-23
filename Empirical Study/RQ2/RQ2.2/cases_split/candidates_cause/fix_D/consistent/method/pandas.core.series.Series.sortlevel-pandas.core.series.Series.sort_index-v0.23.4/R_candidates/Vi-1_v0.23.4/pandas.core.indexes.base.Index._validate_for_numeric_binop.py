    def _validate_for_numeric_binop(self, other, op):
        """
        return valid other, evaluate or raise TypeError
        if we are not of the appropriate type

        internal method called by ops
        """
        opstr = '__{opname}__'.format(opname=op.__name__)
        # if we are an inheritor of numeric,
        # but not actually numeric (e.g. DatetimeIndex/PeriodIndex)
        if not self._is_numeric_dtype:
            raise TypeError("cannot evaluate a numeric op {opstr} "
                            "for type: {typ}"
                            .format(opstr=opstr, typ=type(self).__name__))

        if isinstance(other, Index):
            if not other._is_numeric_dtype:
                raise TypeError("cannot evaluate a numeric op "
                                "{opstr} with type: {typ}"
                                .format(opstr=opstr, typ=type(other)))
        elif isinstance(other, np.ndarray) and not other.ndim:
            other = other.item()

        if isinstance(other, (Index, ABCSeries, np.ndarray)):
            if len(self) != len(other):
                raise ValueError("cannot evaluate a numeric op with "
                                 "unequal lengths")
            other = com._values_from_object(other)
            if other.dtype.kind not in ['f', 'i', 'u']:
                raise TypeError("cannot evaluate a numeric op "
                                "with a non-numeric dtype")
        elif isinstance(other, (ABCDateOffset, np.timedelta64, timedelta)):
            # higher up to handle
            pass
        elif isinstance(other, (datetime, np.datetime64)):
            # higher up to handle
            pass
        else:
            if not (is_float(other) or is_integer(other)):
                raise TypeError("can only perform ops with scalar values")

        return other
