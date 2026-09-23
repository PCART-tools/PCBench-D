    @classmethod
    def _add_numeric_methods_binary(cls):
        """ add in numeric methods, specialized to RangeIndex """

        def _make_evaluate_binop(op, step=False):
            """
            Parameters
            ----------
            op : callable that accepts 2 parms
                perform the binary op
            step : callable, optional, default to False
                op to apply to the step parm if not None
                if False, use the existing step
            """

            def _evaluate_numeric_binop(self, other):
                if isinstance(other, (ABCSeries, ABCDataFrame)):
                    return NotImplemented
                elif isinstance(other, ABCTimedeltaIndex):
                    # Defer to TimedeltaIndex implementation
                    return NotImplemented
                elif isinstance(other, (timedelta, np.timedelta64)):
                    # GH#19333 is_integer evaluated True on timedelta64,
                    # so we need to catch these explicitly
                    return op(self._int64index, other)
                elif is_timedelta64_dtype(other):
                    # Must be an np.ndarray; GH#22390
                    return op(self._int64index, other)

                other = self._validate_for_numeric_binop(other, op)
                attrs = self._get_attributes_dict()
                attrs = self._maybe_update_attributes(attrs)

                left, right = self, other

                try:
                    # apply if we have an override
                    if step:
                        with np.errstate(all='ignore'):
                            rstep = step(left._step, right)

                        # we don't have a representable op
                        # so return a base index
                        if not is_integer(rstep) or not rstep:
                            raise ValueError

                    else:
                        rstep = left._step

                    with np.errstate(all='ignore'):
                        rstart = op(left._start, right)
                        rstop = op(left._stop, right)

                    result = RangeIndex(rstart,
                                        rstop,
                                        rstep,
                                        **attrs)

                    # for compat with numpy / Int64Index
                    # even if we can represent as a RangeIndex, return
                    # as a Float64Index if we have float-like descriptors
                    if not all(is_integer(x) for x in
                               [rstart, rstop, rstep]):
                        result = result.astype('float64')

                    return result

                except (ValueError, TypeError, ZeroDivisionError):
                    # Defer to Int64Index implementation
                    return op(self._int64index, other)
                    # TODO: Do attrs get handled reliably?

            name = '__{name}__'.format(name=op.__name__)
            return compat.set_function_name(_evaluate_numeric_binop, name, cls)

        cls.__add__ = _make_evaluate_binop(operator.add)
        cls.__radd__ = _make_evaluate_binop(ops.radd)
        cls.__sub__ = _make_evaluate_binop(operator.sub)
        cls.__rsub__ = _make_evaluate_binop(ops.rsub)
        cls.__mul__ = _make_evaluate_binop(operator.mul, step=operator.mul)
        cls.__rmul__ = _make_evaluate_binop(ops.rmul, step=ops.rmul)
        cls.__truediv__ = _make_evaluate_binop(operator.truediv,
                                               step=operator.truediv)
        cls.__rtruediv__ = _make_evaluate_binop(ops.rtruediv,
                                                step=ops.rtruediv)
        if not compat.PY3:
            cls.__div__ = _make_evaluate_binop(operator.div, step=operator.div)
            cls.__rdiv__ = _make_evaluate_binop(ops.rdiv, step=ops.rdiv)
