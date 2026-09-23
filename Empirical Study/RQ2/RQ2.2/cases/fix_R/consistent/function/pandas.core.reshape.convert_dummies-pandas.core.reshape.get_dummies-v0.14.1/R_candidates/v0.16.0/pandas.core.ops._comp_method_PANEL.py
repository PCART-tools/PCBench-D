def _comp_method_PANEL(op, name, str_rep=None, masker=False):

    def na_op(x, y):
        try:
            result = expressions.evaluate(op, str_rep, x, y,
                                          raise_on_error=True)
        except TypeError:
            xrav = x.ravel()
            result = np.empty(x.size, dtype=bool)
            if isinstance(y, np.ndarray):
                yrav = y.ravel()
                mask = notnull(xrav) & notnull(yrav)
                result[mask] = op(np.array(list(xrav[mask])),
                                  np.array(list(yrav[mask])))
            else:
                mask = notnull(xrav)
                result[mask] = op(np.array(list(xrav[mask])), y)

            if op == operator.ne:  # pragma: no cover
                np.putmask(result, ~mask, True)
            else:
                np.putmask(result, ~mask, False)
            result = result.reshape(x.shape)

        return result

    @Appender('Wrapper for comparison method %s' % name)
    def f(self, other):
        if isinstance(other, self._constructor):
            return self._compare_constructor(other, na_op)
        elif isinstance(other, (self._constructor_sliced, pd.DataFrame,
                                pd.Series)):
            raise Exception("input needs alignment for this object [%s]" %
                            self._constructor)
        else:
            return self._combine_const(other, na_op)

    f.__name__ = name

    return f
