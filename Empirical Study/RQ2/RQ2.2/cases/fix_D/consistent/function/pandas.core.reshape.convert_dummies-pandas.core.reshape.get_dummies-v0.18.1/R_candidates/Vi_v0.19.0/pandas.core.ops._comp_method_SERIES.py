def _comp_method_SERIES(op, name, str_rep, masker=False):
    """
    Wrapper function for Series arithmetic operations, to avoid
    code duplication.
    """

    def na_op(x, y):

        # dispatch to the categorical if we have a categorical
        # in either operand
        if is_categorical_dtype(x):
            return op(x, y)
        elif is_categorical_dtype(y) and not isscalar(y):
            return op(y, x)

        if is_object_dtype(x.dtype):
            result = _comp_method_OBJECT_ARRAY(op, x, y)
        else:

            # we want to compare like types
            # we only want to convert to integer like if
            # we are not NotImplemented, otherwise
            # we would allow datetime64 (but viewed as i8) against
            # integer comparisons
            if is_datetimelike_v_numeric(x, y):
                raise TypeError("invalid type comparison")

            # numpy does not like comparisons vs None
            if isscalar(y) and isnull(y):
                if name == '__ne__':
                    return np.ones(len(x), dtype=bool)
                else:
                    return np.zeros(len(x), dtype=bool)

            # we have a datetime/timedelta and may need to convert
            mask = None
            if (needs_i8_conversion(x) or
                    (not isscalar(y) and needs_i8_conversion(y))):

                if isscalar(y):
                    mask = isnull(x)
                    y = _index.convert_scalar(x, _values_from_object(y))
                else:
                    mask = isnull(x) | isnull(y)
                    y = y.view('i8')
                x = x.view('i8')

            try:
                with np.errstate(all='ignore'):
                    result = getattr(x, name)(y)
                if result is NotImplemented:
                    raise TypeError("invalid type comparison")
            except AttributeError:
                result = op(x, y)

            if mask is not None and mask.any():
                result[mask] = masker

        return result

    def wrapper(self, other, axis=None):
        # Validate the axis parameter
        if axis is not None:
            self._get_axis_number(axis)

        if isinstance(other, ABCSeries):
            name = _maybe_match_name(self, other)
            if not self._indexed_same(other):
                msg = 'Can only compare identically-labeled Series objects'
                raise ValueError(msg)
            return self._constructor(na_op(self.values, other.values),
                                     index=self.index, name=name)
        elif isinstance(other, pd.DataFrame):  # pragma: no cover
            return NotImplemented
        elif isinstance(other, (np.ndarray, pd.Index)):
            # do not check length of zerodim array
            # as it will broadcast
            if (not lib.isscalar(lib.item_from_zerodim(other)) and
                    len(self) != len(other)):
                raise ValueError('Lengths must match to compare')

            if isinstance(other, ABCPeriodIndex):
                # temp workaround until fixing GH 13637
                # tested in test_nat_comparisons
                # (pandas.tests.series.test_operators.TestSeriesOperators)
                return self._constructor(na_op(self.values,
                                               other.asobject.values),
                                         index=self.index)

            return self._constructor(na_op(self.values, np.asarray(other)),
                                     index=self.index).__finalize__(self)

        elif isinstance(other, pd.Categorical):
            if not is_categorical_dtype(self):
                msg = ("Cannot compare a Categorical for op {op} with Series "
                       "of dtype {typ}.\nIf you want to compare values, use "
                       "'series <op> np.asarray(other)'.")
                raise TypeError(msg.format(op=op, typ=self.dtype))

        if is_categorical_dtype(self):
            # cats are a special case as get_values() would return an ndarray,
            # which would then not take categories ordering into account
            # we can go directly to op, as the na_op would just test again and
            # dispatch to it.
            with np.errstate(all='ignore'):
                res = op(self.values, other)
        else:
            values = self.get_values()
            if isinstance(other, (list, np.ndarray)):
                other = np.asarray(other)

            with np.errstate(all='ignore'):
                res = na_op(values, other)
            if isscalar(res):
                raise TypeError('Could not compare %s type with Series' %
                                type(other))

            # always return a full value series here
            res = _values_from_object(res)

        res = pd.Series(res, index=self.index, name=self.name, dtype='bool')
        return res

    return wrapper
