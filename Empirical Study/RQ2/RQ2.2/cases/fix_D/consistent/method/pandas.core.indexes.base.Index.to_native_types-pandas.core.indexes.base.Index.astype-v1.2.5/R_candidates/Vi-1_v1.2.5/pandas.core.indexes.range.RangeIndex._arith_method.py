    def _arith_method(self, other, op):
        """
        Parameters
        ----------
        other : Any
        op : callable that accepts 2 params
            perform the binary op
        """

        if isinstance(other, ABCTimedeltaIndex):
            # Defer to TimedeltaIndex implementation
            return NotImplemented
        elif isinstance(other, (timedelta, np.timedelta64)):
            # GH#19333 is_integer evaluated True on timedelta64,
            # so we need to catch these explicitly
            return op(self._int64index, other)
        elif is_timedelta64_dtype(other):
            # Must be an np.ndarray; GH#22390
            return op(self._int64index, other)

        if op in [
            operator.pow,
            ops.rpow,
            operator.mod,
            ops.rmod,
            ops.rfloordiv,
            divmod,
            ops.rdivmod,
        ]:
            return op(self._int64index, other)

        step = False
        if op in [operator.mul, ops.rmul, operator.truediv, ops.rtruediv]:
            step = op

        other = extract_array(other, extract_numpy=True)
        attrs = self._get_attributes_dict()

        left, right = self, other

        try:
            # apply if we have an override
            if step:
                with np.errstate(all="ignore"):
                    rstep = step(left.step, right)

                # we don't have a representable op
                # so return a base index
                if not is_integer(rstep) or not rstep:
                    raise ValueError

            else:
                rstep = left.step

            with np.errstate(all="ignore"):
                rstart = op(left.start, right)
                rstop = op(left.stop, right)

            result = type(self)(rstart, rstop, rstep, **attrs)

            # for compat with numpy / Int64Index
            # even if we can represent as a RangeIndex, return
            # as a Float64Index if we have float-like descriptors
            if not all(is_integer(x) for x in [rstart, rstop, rstep]):
                result = result.astype("float64")

            return result

        except (ValueError, TypeError, ZeroDivisionError):
            # Defer to Int64Index implementation
            return op(self._int64index, other)
