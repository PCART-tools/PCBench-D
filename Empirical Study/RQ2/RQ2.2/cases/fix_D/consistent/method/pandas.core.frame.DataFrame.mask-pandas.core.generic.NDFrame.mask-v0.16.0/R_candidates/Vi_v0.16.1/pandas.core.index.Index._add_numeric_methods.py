    @classmethod
    def _add_numeric_methods(cls):
        """ add in numeric methods """

        def _make_evaluate_binop(op, opstr, reversed=False):

            def _evaluate_numeric_binop(self, other):
                import pandas.tseries.offsets as offsets

                # if we are an inheritor of numeric, but not actually numeric (e.g. DatetimeIndex/PeriodInde)
                if not self._is_numeric_dtype:
                    raise TypeError("cannot evaluate a numeric op {opstr} for type: {typ}".format(opstr=opstr,
                                                                                                  typ=type(self)))

                if isinstance(other, Index):
                    if not other._is_numeric_dtype:
                        raise TypeError("cannot evaluate a numeric op {opstr} with type: {typ}".format(opstr=type(self),
                                                                                                       typ=type(other)))
                elif isinstance(other, np.ndarray) and not other.ndim:
                    other = other.item()

                if isinstance(other, (Index, ABCSeries, np.ndarray)):
                    if len(self) != len(other):
                        raise ValueError("cannot evaluate a numeric op with unequal lengths")
                    other = _values_from_object(other)
                    if other.dtype.kind not in ['f','i']:
                        raise TypeError("cannot evaluate a numeric op with a non-numeric dtype")
                elif isinstance(other, (offsets.DateOffset, np.timedelta64, Timedelta, datetime.timedelta)):
                    return self._evaluate_with_timedelta_like(other, op, opstr)
                elif isinstance(other, (Timestamp, np.datetime64)):
                    return self._evaluate_with_datetime_like(other, op, opstr)
                else:
                    if not (is_float(other) or is_integer(other)):
                        raise TypeError("can only perform ops with scalar values")

                # if we are a reversed non-communative op
                values = self.values
                if reversed:
                    values, other = other, values

                return self._shallow_copy(op(values, other))

            return _evaluate_numeric_binop

        def _make_evaluate_unary(op, opstr):

            def _evaluate_numeric_unary(self):

                # if we are an inheritor of numeric, but not actually numeric (e.g. DatetimeIndex/PeriodInde)
                if not self._is_numeric_dtype:
                    raise TypeError("cannot evaluate a numeric op {opstr} for type: {typ}".format(opstr=opstr,
                                                                                                  typ=type(self)))

                return self._shallow_copy(op(self.values))

            return _evaluate_numeric_unary

        cls.__add__ = cls.__radd__ = _make_evaluate_binop(operator.add,'__add__')
        cls.__sub__ = _make_evaluate_binop(operator.sub,'__sub__')
        cls.__rsub__ = _make_evaluate_binop(operator.sub,'__sub__',reversed=True)
        cls.__mul__ = cls.__rmul__ = _make_evaluate_binop(operator.mul,'__mul__')
        cls.__floordiv__ = _make_evaluate_binop(operator.floordiv,'__floordiv__')
        cls.__rfloordiv__ = _make_evaluate_binop(operator.floordiv,'__floordiv__',reversed=True)
        cls.__truediv__ = _make_evaluate_binop(operator.truediv,'__truediv__')
        cls.__rtruediv__ = _make_evaluate_binop(operator.truediv,'__truediv__',reversed=True)
        if not compat.PY3:
            cls.__div__ = _make_evaluate_binop(operator.div,'__div__')
            cls.__rdiv__ = _make_evaluate_binop(operator.div,'__div__',reversed=True)
        cls.__neg__ = _make_evaluate_unary(lambda x: -x,'__neg__')
        cls.__pos__ = _make_evaluate_unary(lambda x: x,'__pos__')
        cls.__abs__ = _make_evaluate_unary(lambda x: np.abs(x),'__abs__')
        cls.__inv__ = _make_evaluate_unary(lambda x: -x,'__inv__')
