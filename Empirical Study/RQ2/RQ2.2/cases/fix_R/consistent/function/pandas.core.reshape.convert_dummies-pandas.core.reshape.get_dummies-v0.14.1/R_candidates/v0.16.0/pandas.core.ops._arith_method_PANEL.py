def _arith_method_PANEL(op, name, str_rep=None, fill_zeros=None,
                        default_axis=None, **eval_kwargs):
    # copied from Series na_op above, but without unnecessary branch for
    # non-scalar
    def na_op(x, y):
        try:
            result = expressions.evaluate(op, str_rep, x, y,
                                          raise_on_error=True, **eval_kwargs)
        except TypeError:

            # TODO: might need to find_common_type here?
            result = np.empty(len(x), dtype=x.dtype)
            mask = notnull(x)
            result[mask] = op(x[mask], y)
            result, changed = com._maybe_upcast_putmask(result, ~mask, np.nan)

        result = com._fill_zeros(result, x, y, name, fill_zeros)
        return result

    # work only for scalars
    def f(self, other):
        if not np.isscalar(other):
            raise ValueError('Simple arithmetic with %s can only be '
                             'done with scalar values' %
                             self._constructor.__name__)

        return self._combine(other, op)
    f.__name__ = name
    return f
