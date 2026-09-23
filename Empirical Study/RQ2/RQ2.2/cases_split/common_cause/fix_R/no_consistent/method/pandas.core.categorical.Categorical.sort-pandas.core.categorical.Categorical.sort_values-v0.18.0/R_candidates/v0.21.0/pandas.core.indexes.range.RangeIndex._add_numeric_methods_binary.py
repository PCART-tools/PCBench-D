    @classmethod
    def _add_numeric_methods_binary(cls):
        """ add in numeric methods, specialized to RangeIndex """

        def _make_evaluate_binop(op, opstr, reversed=False, step=False):
            """
            Parameters
            ----------
            op : callable that accepts 2 parms
                perform the binary op
            opstr : string
                string name of ops
            reversed : boolean, default False
                if this is a reversed op, e.g. radd
            step : callable, optional, default to False
                op to apply to the step parm if not None
                if False, use the existing step
            """

            def _evaluate_numeric_binop(self, other):

                other = self._validate_for_numeric_binop(other, op, opstr)
                attrs = self._get_attributes_dict()
                attrs = self._maybe_update_attributes(attrs)

                if reversed:
                    self, other = other, self

                try:
                    # alppy if we have an override
                    if step:
                        with np.errstate(all='ignore'):
                            rstep = step(self._step, other)

                        # we don't have a representable op
                        # so return a base index
                        if not is_integer(rstep) or not rstep:
                            raise ValueError

                    else:
                        rstep = self._step

                    with np.errstate(all='ignore'):
                        rstart = op(self._start, other)
                        rstop = op(self._stop, other)

                    result = RangeIndex(rstart,
                                        rstop,
                                        rstep,
                                        **attrs)

                    # for compat with numpy / Int64Index
                    # even if we can represent as a RangeIndex, return
                    # as a Float64Index if we have float-like descriptors
                    if not all([is_integer(x) for x in
                                [rstart, rstop, rstep]]):
                        result = result.astype('float64')

                    return result

                except (ValueError, TypeError, AttributeError):
                    pass

                # convert to Int64Index ops
                if isinstance(self, RangeIndex):
                    self = self.values
                if isinstance(other, RangeIndex):
                    other = other.values

                with np.errstate(all='ignore'):
                    results = op(self, other)
                return Index(results, **attrs)

            return _evaluate_numeric_binop

        cls.__add__ = cls.__radd__ = _make_evaluate_binop(
            operator.add, '__add__')
        cls.__sub__ = _make_evaluate_binop(operator.sub, '__sub__')
        cls.__rsub__ = _make_evaluate_binop(
            operator.sub, '__sub__', reversed=True)
        cls.__mul__ = cls.__rmul__ = _make_evaluate_binop(
            operator.mul,
            '__mul__',
            step=operator.mul)
        cls.__truediv__ = _make_evaluate_binop(
            operator.truediv,
            '__truediv__',
            step=operator.truediv)
        cls.__rtruediv__ = _make_evaluate_binop(
            operator.truediv,
            '__truediv__',
            reversed=True,
            step=operator.truediv)
        if not compat.PY3:
            cls.__div__ = _make_evaluate_binop(
                operator.div,
                '__div__',
                step=operator.div)
            cls.__rdiv__ = _make_evaluate_binop(
                operator.div,
                '__div__',
                reversed=True,
                step=operator.div)
