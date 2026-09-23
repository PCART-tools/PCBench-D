def _comp_method_SERIES(op, name, str_rep, masker=False):
    """
    Wrapper function for Series arithmetic operations, to avoid
    code duplication.
    """
    def na_op(x, y):

        # dispatch to the categorical if we have a categorical
        # in either operand
        if com.is_categorical_dtype(x):
            return op(x,y)
        elif com.is_categorical_dtype(y) and not lib.isscalar(y):
            return op(y,x)

        if x.dtype == np.object_:
            if isinstance(y, list):
                y = lib.list_to_object_array(y)

            if isinstance(y, (np.ndarray, pd.Series)):
                if y.dtype != np.object_:
                    result = lib.vec_compare(x, y.astype(np.object_), op)
                else:
                    result = lib.vec_compare(x, y, op)
            else:
                result = lib.scalar_compare(x, y, op)
        else:

            try:
                result = getattr(x, name)(y)
                if result is NotImplemented:
                    raise TypeError("invalid type comparison")
            except (AttributeError):
                result = op(x, y)

        return result

    def wrapper(self, other):
        if isinstance(other, pd.Series):
            name = _maybe_match_name(self, other)
            if len(self) != len(other):
                raise ValueError('Series lengths must match to compare')
            return self._constructor(na_op(self.values, other.values),
                                     index=self.index, name=name)
        elif isinstance(other, pd.DataFrame):  # pragma: no cover
            return NotImplemented
        elif isinstance(other, (np.ndarray, pd.Index)):
            if len(self) != len(other):
                raise ValueError('Lengths must match to compare')
            return self._constructor(na_op(self.values, np.asarray(other)),
                                     index=self.index).__finalize__(self)
        elif isinstance(other, pd.Categorical):
            if not com.is_categorical_dtype(self):
                msg = "Cannot compare a Categorical for op {op} with Series of dtype {typ}.\n"\
                      "If you want to compare values, use 'series <op> np.asarray(other)'."
                raise TypeError(msg.format(op=op,typ=self.dtype))


        mask = isnull(self)

        values = self.get_values()
        other = _index.convert_scalar(values,_values_from_object(other))

        if issubclass(values.dtype.type, (np.datetime64, np.timedelta64)):
            values = values.view('i8')

        # scalars
        res = na_op(values, other)
        if np.isscalar(res):
            raise TypeError('Could not compare %s type with Series'
                            % type(other))

        # always return a full value series here
        res = _values_from_object(res)

        res = pd.Series(res, index=self.index, name=self.name,
                        dtype='bool')

        # mask out the invalids
        if mask.any():
            res[mask] = masker

        return res
    return wrapper
