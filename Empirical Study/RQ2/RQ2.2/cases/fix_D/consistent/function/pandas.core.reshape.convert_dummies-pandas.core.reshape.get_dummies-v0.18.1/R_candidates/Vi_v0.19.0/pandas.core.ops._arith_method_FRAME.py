def _arith_method_FRAME(op, name, str_rep=None, default_axis='columns',
                        fill_zeros=None, **eval_kwargs):
    def na_op(x, y):
        try:
            result = expressions.evaluate(op, str_rep, x, y,
                                          raise_on_error=True, **eval_kwargs)
        except TypeError:
            xrav = x.ravel()
            if isinstance(y, (np.ndarray, ABCSeries)):
                dtype = np.find_common_type([x.dtype, y.dtype], [])
                result = np.empty(x.size, dtype=dtype)
                yrav = y.ravel()
                mask = notnull(xrav) & notnull(yrav)
                xrav = xrav[mask]
                yrav = yrav[mask]
                if np.prod(xrav.shape) and np.prod(yrav.shape):
                    with np.errstate(all='ignore'):
                        result[mask] = op(xrav, yrav)
            elif hasattr(x, 'size'):
                result = np.empty(x.size, dtype=x.dtype)
                mask = notnull(xrav)
                xrav = xrav[mask]
                if np.prod(xrav.shape):
                    with np.errstate(all='ignore'):
                        result[mask] = op(xrav, y)
            else:
                raise TypeError("cannot perform operation {op} between "
                                "objects of type {x} and {y}".format(
                                    op=name, x=type(x), y=type(y)))

            result, changed = _maybe_upcast_putmask(result, ~mask, np.nan)
            result = result.reshape(x.shape)

        result = missing.fill_zeros(result, x, y, name, fill_zeros)

        return result

    if name in _op_descriptions:
        op_name = name.replace('__', '')
        op_desc = _op_descriptions[op_name]
        if op_desc['reversed']:
            equiv = 'other ' + op_desc['op'] + ' dataframe'
        else:
            equiv = 'dataframe ' + op_desc['op'] + ' other'

        doc = _flex_doc_FRAME % (op_desc['desc'], op_name, equiv,
                                 op_desc['reverse'])
    else:
        doc = _arith_doc_FRAME % name

    @Appender(doc)
    def f(self, other, axis=default_axis, level=None, fill_value=None):

        other = _align_method_FRAME(self, other, axis)

        if isinstance(other, pd.DataFrame):  # Another DataFrame
            return self._combine_frame(other, na_op, fill_value, level)
        elif isinstance(other, ABCSeries):
            return self._combine_series(other, na_op, fill_value, axis, level)
        else:
            if fill_value is not None:
                self = self.fillna(fill_value)

            return self._combine_const(other, na_op)

    f.__name__ = name

    return f
