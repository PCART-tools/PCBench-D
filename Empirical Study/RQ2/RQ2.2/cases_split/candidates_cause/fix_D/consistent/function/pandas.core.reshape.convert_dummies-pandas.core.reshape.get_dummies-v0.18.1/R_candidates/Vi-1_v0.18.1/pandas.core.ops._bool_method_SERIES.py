def _bool_method_SERIES(op, name, str_rep):
    """
    Wrapper function for Series arithmetic operations, to avoid
    code duplication.
    """

    def na_op(x, y):
        try:
            result = op(x, y)
        except TypeError:
            if isinstance(y, list):
                y = lib.list_to_object_array(y)

            if isinstance(y, (np.ndarray, ABCSeries)):
                if (is_bool_dtype(x.dtype) and is_bool_dtype(y.dtype)):
                    result = op(x, y)  # when would this be hit?
                else:
                    x = com._ensure_object(x)
                    y = com._ensure_object(y)
                    result = lib.vec_binop(x, y, op)
            else:
                try:

                    # let null fall thru
                    if not isnull(y):
                        y = bool(y)
                    result = lib.scalar_binop(x, y, op)
                except:
                    raise TypeError("cannot compare a dtyped [{0}] array with "
                                    "a scalar of type [{1}]".format(
                                        x.dtype, type(y).__name__))

        return result

    def wrapper(self, other):
        is_self_int_dtype = is_integer_dtype(self.dtype)

        fill_int = lambda x: x.fillna(0)
        fill_bool = lambda x: x.fillna(False).astype(bool)

        if isinstance(other, ABCSeries):
            name = _maybe_match_name(self, other)
            other = other.reindex_like(self)
            is_other_int_dtype = is_integer_dtype(other.dtype)
            other = fill_int(other) if is_other_int_dtype else fill_bool(other)

            filler = (fill_int if is_self_int_dtype and is_other_int_dtype
                      else fill_bool)
            return filler(self._constructor(na_op(self.values, other.values),
                                            index=self.index, name=name))

        elif isinstance(other, pd.DataFrame):
            return NotImplemented

        else:
            # scalars, list, tuple, np.array
            filler = (fill_int if is_self_int_dtype and
                      is_integer_dtype(np.asarray(other)) else fill_bool)
            return filler(self._constructor(
                na_op(self.values, other),
                index=self.index)).__finalize__(self)

    return wrapper
