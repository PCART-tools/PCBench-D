    @classmethod
    def _add_numeric_methods_binary(cls):
        """ add in numeric methods """

        def _make_evaluate_binop(op, opstr, reversed=False, constructor=Index):
            def _evaluate_numeric_binop(self, other):

                from pandas.tseries.offsets import DateOffset
                other = self._validate_for_numeric_binop(other, op, opstr)

                # handle time-based others
                if isinstance(other, (DateOffset, np.timedelta64,
                                      Timedelta, datetime.timedelta)):
                    return self._evaluate_with_timedelta_like(other, op, opstr)
                elif isinstance(other, (Timestamp, np.datetime64)):
                    return self._evaluate_with_datetime_like(other, op, opstr)

                # if we are a reversed non-communative op
                values = self.values
                if reversed:
                    values, other = other, values

                attrs = self._get_attributes_dict()
                attrs = self._maybe_update_attributes(attrs)
                with np.errstate(all='ignore'):
                    result = op(values, other)
                return constructor(result, **attrs)

            return _evaluate_numeric_binop

        cls.__add__ = cls.__radd__ = _make_evaluate_binop(
            operator.add, '__add__')
        cls.__sub__ = _make_evaluate_binop(
            operator.sub, '__sub__')
        cls.__rsub__ = _make_evaluate_binop(
            operator.sub, '__sub__', reversed=True)
        cls.__mul__ = cls.__rmul__ = _make_evaluate_binop(
            operator.mul, '__mul__')
        cls.__rpow__ = _make_evaluate_binop(
            operator.pow, '__pow__', reversed=True)
        cls.__pow__ = _make_evaluate_binop(
            operator.pow, '__pow__')
        cls.__mod__ = _make_evaluate_binop(
            operator.mod, '__mod__')
        cls.__floordiv__ = _make_evaluate_binop(
            operator.floordiv, '__floordiv__')
        cls.__rfloordiv__ = _make_evaluate_binop(
            operator.floordiv, '__floordiv__', reversed=True)
        cls.__truediv__ = _make_evaluate_binop(
            operator.truediv, '__truediv__')
        cls.__rtruediv__ = _make_evaluate_binop(
            operator.truediv, '__truediv__', reversed=True)
        if not compat.PY3:
            cls.__div__ = _make_evaluate_binop(
                operator.div, '__div__')
            cls.__rdiv__ = _make_evaluate_binop(
                operator.div, '__div__', reversed=True)

        cls.__divmod__ = _make_evaluate_binop(
            divmod,
            '__divmod__',
            constructor=lambda result, **attrs: (
                Index(result[0], **attrs),
                Index(result[1], **attrs),
            ),
        )
