def _arith_method_SERIES(op, name, str_rep, fill_zeros=None, default_axis=None,
                         construct_result=_construct_result, **eval_kwargs):
    """
    Wrapper function for Series arithmetic operations, to avoid
    code duplication.
    """

    def na_op(x, y):
        try:
            result = expressions.evaluate(op, str_rep, x, y,
                                          raise_on_error=True, **eval_kwargs)
        except TypeError:
            if isinstance(y, (np.ndarray, ABCSeries, pd.Index)):
                dtype = _find_common_type([x.dtype, y.dtype])
                result = np.empty(x.size, dtype=dtype)
                mask = notnull(x) & notnull(y)
                result[mask] = op(x[mask], _values_from_object(y[mask]))
            elif isinstance(x, np.ndarray):
                result = np.empty(len(x), dtype=x.dtype)
                mask = notnull(x)
                result[mask] = op(x[mask], y)
            else:
                raise TypeError("{typ} cannot perform the operation "
                                "{op}".format(typ=type(x).__name__,
                                              op=str_rep))

            result, changed = _maybe_upcast_putmask(result, ~mask, np.nan)

        result = missing.fill_zeros(result, x, y, name, fill_zeros)
        return result

    def safe_na_op(lvalues, rvalues):
        try:
            with np.errstate(all='ignore'):
                return na_op(lvalues, rvalues)
        except Exception:
            if isinstance(rvalues, ABCSeries):
                if is_object_dtype(rvalues):
                    # if dtype is object, try elementwise op
                    return _algos.arrmap_object(rvalues,
                                                lambda x: op(lvalues, x))
            else:
                if is_object_dtype(lvalues):
                    return _algos.arrmap_object(lvalues,
                                                lambda x: op(x, rvalues))
            raise

    def wrapper(left, right, name=name, na_op=na_op):

        if isinstance(right, pd.DataFrame):
            return NotImplemented

        left, right = _align_method_SERIES(left, right)

        converted = _Op.get_op(left, right, name, na_op)

        left, right = converted.left, converted.right
        lvalues, rvalues = converted.lvalues, converted.rvalues
        dtype = converted.dtype
        wrap_results = converted.wrap_results
        na_op = converted.na_op

        if isinstance(rvalues, ABCSeries):
            name = _maybe_match_name(left, rvalues)
            lvalues = getattr(lvalues, 'values', lvalues)
            rvalues = getattr(rvalues, 'values', rvalues)
            # _Op aligns left and right
        else:
            name = left.name
            if (hasattr(lvalues, 'values') and
                    not isinstance(lvalues, pd.DatetimeIndex)):
                lvalues = lvalues.values

        result = wrap_results(safe_na_op(lvalues, rvalues))
        return construct_result(
            left,
            result,
            index=left.index,
            name=name,
            dtype=dtype,
        )

    return wrapper
