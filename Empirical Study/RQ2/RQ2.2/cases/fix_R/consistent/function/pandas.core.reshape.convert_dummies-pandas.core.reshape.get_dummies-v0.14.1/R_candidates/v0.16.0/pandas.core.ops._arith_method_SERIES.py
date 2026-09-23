def _arith_method_SERIES(op, name, str_rep, fill_zeros=None,
                         default_axis=None, **eval_kwargs):
    """
    Wrapper function for Series arithmetic operations, to avoid
    code duplication.
    """
    def na_op(x, y):
        try:
            result = expressions.evaluate(op, str_rep, x, y,
                                          raise_on_error=True, **eval_kwargs)
        except TypeError:
            if isinstance(y, (np.ndarray, pd.Series, pd.Index)):
                dtype = np.find_common_type([x.dtype, y.dtype], [])
                result = np.empty(x.size, dtype=dtype)
                mask = notnull(x) & notnull(y)
                result[mask] = op(x[mask], _values_from_object(y[mask]))
            elif isinstance(x, np.ndarray):
                result = np.empty(len(x), dtype=x.dtype)
                mask = notnull(x)
                result[mask] = op(x[mask], y)
            else:
                raise TypeError("{typ} cannot perform the operation {op}".format(typ=type(x).__name__,op=str_rep))

            result, changed = com._maybe_upcast_putmask(result, ~mask, np.nan)

        result = com._fill_zeros(result, x, y, name, fill_zeros)
        return result

    def wrapper(left, right, name=name):

        if isinstance(right, pd.DataFrame):
            return NotImplemented

        time_converted = _TimeOp.maybe_convert_for_time_op(left, right, name)

        if time_converted is None:
            lvalues, rvalues = left, right
            dtype = None
            wrap_results = lambda x: x
        elif time_converted == NotImplemented:
            return NotImplemented
        else:
            left, right = time_converted.left, time_converted.right
            lvalues, rvalues = time_converted.lvalues, time_converted.rvalues
            dtype = time_converted.dtype
            wrap_results = time_converted.wrap_results

        if isinstance(rvalues, pd.Series):
            rindex = getattr(rvalues,'index',rvalues)
            name = _maybe_match_name(left, rvalues)
            lvalues = getattr(lvalues, 'values', lvalues)
            rvalues = getattr(rvalues, 'values', rvalues)
            if left.index.equals(rindex):
                index = left.index
            else:
                index, lidx, ridx = left.index.join(rindex, how='outer',
                                                       return_indexers=True)

                if lidx is not None:
                    lvalues = com.take_1d(lvalues, lidx)

                if ridx is not None:
                    rvalues = com.take_1d(rvalues, ridx)

            arr = na_op(lvalues, rvalues)

            return left._constructor(wrap_results(arr), index=index,
                                     name=name, dtype=dtype)
        else:
            # scalars
            if hasattr(lvalues, 'values'):
                lvalues = lvalues.values
            return left._constructor(wrap_results(na_op(lvalues, rvalues)),
                                     index=left.index, name=left.name,
                                     dtype=dtype)
    return wrapper
